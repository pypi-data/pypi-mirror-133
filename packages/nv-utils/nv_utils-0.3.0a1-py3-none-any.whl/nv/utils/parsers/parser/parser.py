from collections.abc import Mapping, Sequence, MutableSequence, Set, MutableSet
from enum import Enum
from functools import partial
from typing import Callable, Any, Iterable, Protocol, Optional, Collection, Tuple


__ALL__ = ['build_parser', 'build_parsers_map', 'build_strict_parser', 'build_safe_parser', 'as_element_parser',
           'remove_all', 'remove_empty']


class InternalParser(Protocol):
    def __call__(self, obj: Any, parser: 'InternalParser', **kwargs) -> Any:
        pass


class Parser(Protocol):
    def __call__(self, obj: Any, **kwargs) -> Any:
        pass


ParsingMap = Sequence[Tuple[type, InternalParser]]


# Definitions for parsing behaviour
BASIC_TYPES = (
    int,
    float,
    complex,
    bool,
    type(None),
)


BASIC_SEQUENCES = (
    str,
    bytes,
    bytearray,
)

# Types parsed as a single element
BASIC_ELEMENTS = (
    *BASIC_TYPES,
    *BASIC_SEQUENCES,
)

# Types whose elements will be parsed individually into one of the basic sructures
BASIC_COLLECTIONS = (
    MutableSet,
    Set,
    MutableSequence,
    Sequence,
    Mapping,
)


class ObjectWrapper:
    def __init__(self, content, mark_empty=False):
        self.content = content
        self.mark_empty = mark_empty

    def __bool__(self):
        if self.mark_empty:
            return False
        return bool(self.content)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.content!r})"


class UnknownObject(ObjectWrapper):
    pass


class RemoveObject(ObjectWrapper):
    pass


class UnknownParser:
    """
    Drives the behaviour of unknown parser.
    """

    class Behaviour(int, Enum):
        IGNORE = 0
        MARK = 1
        REPLACE = 2
        REMOVE = 3
        RAISE = 255

    REPLACEMENT = None

    DEFAULT = object()

    @classmethod
    def match_behaviour(cls, behaviour: 'UnknownParser.Behaviour', obj: Any, replacement: Any | None = DEFAULT):
        match behaviour:
            case cls.Behaviour.IGNORE:
                return obj
            case cls.Behaviour.REPLACE:
                return cls.REPLACEMENT if replacement is cls.DEFAULT else replacement
            case cls.Behaviour.REMOVE:
                return RemoveObject(obj)
            case cls.Behaviour.MARK:
                return UnknownObject(obj)
            case cls.Behaviour.RAISE:
                raise TypeError(f"unable to parse {type(obj)} in {obj!r}")
            case _:
                raise ValueError(f"undefined behaviour for UnknownParser: {behaviour}.")

    @classmethod
    def build_unknown_parser_handler(cls, behaviour: 'UnknownParser.Behaviour',
                                     replacement: Any | None = DEFAULT) -> InternalParser:

        def handle_unknown_parser(obj, _: InternalParser, **kwargs):
            return cls.match_behaviour(behaviour, obj, replacement=replacement)
        return handle_unknown_parser


def as_element_parser(p=None, **build_kwargs):
    if p is None:
        return partial(as_element_parser, **build_kwargs)

    def parser(obj: Any, _, *, wrapper: Optional[Callable] = None, **kwargs: Any) -> Any:
        result = p(obj, **build_kwargs)
        return result if wrapper is None else wrapper(result)

    return parser


def collection_parser(collection_type, iterable: Iterable, parser: InternalParser, *,
                      wrapper: Optional[Callable] = None, **kwargs):

    result = collection_type(
        pi for pi in (
            parser(i, parser, wrapper=wrapper, **kwargs) for i in iterable
        ) if not isinstance(pi, RemoveObject)
    )
    return result if wrapper is None else wrapper(result)


def mapping_parser(mapping_type: type, mapping: Mapping, parser: InternalParser, *,
                   wrapper: Optional[Callable] = None, parse_keys=False, **kwargs):

    result = mapping_type(
        (pk, pv) for pk, pv in (
            (parser(k, parser, wrapper=wrapper, parse_keys=parse_keys, **kwargs) if parse_keys else k,
             parser(v, parser, wrapper=wrapper, parse_keys=parse_keys, **kwargs)) for k, v in mapping.items()
        ) if not isinstance(pk, RemoveObject) and not isinstance(pv, RemoveObject)
    )

    return result if wrapper is None else wrapper(result)


def parse_mutable_set(obj: MutableSet, p: InternalParser, **kwargs) -> set:
    return collection_parser(set, obj, p, **kwargs)


def parse_frozen_set(obj: MutableSet, p: InternalParser, **kwargs) -> frozenset:
    return collection_parser(frozenset, obj, p, **kwargs)


def parse_mutable_sequence(obj: MutableSet, p: InternalParser, **kwargs) -> list:
    return collection_parser(list, obj, p, **kwargs)


def parse_sequence(obj: MutableSet, p: InternalParser, **kwargs) -> tuple:
    return collection_parser(tuple, obj, p, **kwargs)


def parse_mapping(obj: Mapping, p: InternalParser, **kwargs) -> dict:
    return mapping_parser(dict, obj, p, **kwargs)


COLLECTION_PARSERS = (
    (MutableSet, parse_mutable_set),
    (Set, parse_frozen_set),
    (MutableSequence, parse_mutable_sequence),
    (Sequence, parse_sequence),
    (Mapping, parse_mapping),
)


def build_parsing_map(element_parser: InternalParser, elements=BASIC_ELEMENTS,
                      collection_parsers=COLLECTION_PARSERS) -> ParsingMap:
    return (
        (elements, element_parser),
        *collection_parsers,
    )


def select_parser(obj,
                  parsing_map: ParsingMap,
                  behaviour: UnknownParser.Behaviour.RAISE,
                  replacement: Any | None = UnknownParser.DEFAULT,
                  default_parser: InternalParser = None
                  ) -> InternalParser:

    parser = next((p for t, p in parsing_map if isinstance(obj, t)),
                  None
                  )

    return parser or default_parser or UnknownParser.build_unknown_parser_handler(behaviour=behaviour,
                                                                                  replacement=replacement)


def build_parser_from_map(parsing_map,
                          behaviour: UnknownParser.Behaviour = UnknownParser.Behaviour.RAISE,
                          replacement: Any | None = UnknownParser.DEFAULT,
                          default_parser: Optional[InternalParser] = None,
                          wrapper: Optional[Callable] = None,
                          **build_kwargs: Any) -> Parser:

    def _internal_parser(obj, parser: InternalParser, *, wrapper=wrapper, **kwargs):
        kwargs = kwargs | build_kwargs
        selected_parser = select_parser(obj, parsing_map, behaviour, replacement=replacement,
                                        default_parser=default_parser)
        result = selected_parser(obj, parser, wrapper=wrapper, **(build_kwargs | kwargs))
        return result

    def _parser(obj, **parser_kwargs):
        result = _internal_parser(obj, _internal_parser, wrapper=wrapper, **(parser_kwargs | build_kwargs))
        return result if not isinstance(result, RemoveObject) else None

    return _parser


def build_parser(element_parser,
                 elements=BASIC_ELEMENTS,
                 collection_parsers=COLLECTION_PARSERS,
                 **build_kwargs
                 ) -> Parser:
    parsing_map = build_parsing_map(element_parser, elements=elements, collection_parsers=collection_parsers)
    return build_parser_from_map(parsing_map, **build_kwargs)


build_strict_parser: Parser = partial(build_parser, behaviour=UnknownParser.Behaviour.RAISE)
build_safe_parser: Parser = partial(build_parser, behavior=UnknownParser.Behaviour.IGNORE)


# Useful wrappers for cleaning None and empty stuff
def build_single_wrapper(*wrappers):
    def _wrapper(obj):
        for wrapper in wrappers:
            obj = wrapper(obj)
        return obj
    return _wrapper


def remove_empty_collections(obj: Any) -> Any:
    if isinstance(obj, BASIC_COLLECTIONS) and len(obj) == 0:
        return RemoveObject(obj)
    return obj


def remove_empty_strings(obj: Any) -> Any:
    if isinstance(obj, BASIC_SEQUENCES) and len(obj) == 0:
        return RemoveObject(obj)
    return obj


def remove_none_objects(obj: Any) -> Any:
    if obj is None:
        return RemoveObject(obj)
    return obj


ALL_REMOVERS = (
    remove_none_objects,
    remove_empty_strings,
    remove_empty_collections,
)


EMPTY_REMOVERS = (
    remove_empty_strings,
    remove_empty_collections,
)


remove_all = build_single_wrapper(*ALL_REMOVERS)
remove_empty = build_single_wrapper(*EMPTY_REMOVERS)

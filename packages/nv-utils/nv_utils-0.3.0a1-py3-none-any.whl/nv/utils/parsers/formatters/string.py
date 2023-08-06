from collections.abc import Mapping
from enum import IntFlag
from functools import partial
import string
from typing import Sequence, Any, Callable, MutableSet

from nv.utils.parsers.parser import (build_parsing_map, build_parser_from_map, as_element_parser,
                                     remove_none_objects, remove_empty_strings, remove_empty_collections, UnknownParser,
                                     InternalParser)
from nv.utils.collections import MissingKey, SafeDictWrapper, SafeDictWrapperWithTracker


__ALL__ = ['StringFormatter']


class SafeFormatter(string.Formatter):
    def check_unused_args(self, used_args: Sequence[int | str],
                          args: Sequence[Any], kwargs: Mapping[str, Any]) -> None:
        # This function is supposed to raise problems when a key is not used, but was overwritten to do nothing
        pass


def safe_format(s: str, mapping: Mapping) -> str:
    return SafeFormatter().vformat(s, (), mapping)


class CleanUp:
    class Behaviour(IntFlag):
        NO_CLEANUP = 0
        NONE = 1
        EMPTY_STRING = 2
        EMPTY_COLLECTIONS = 4
        EMPTY = 6
        ALL = 255

    @classmethod
    def cleanup(cls, obj: Any, behaviour: Behaviour = Behaviour.ALL) -> Any | None:
        if behaviour & cls.Behaviour.NONE:
            obj = remove_none_objects(obj)
        if behaviour & cls.Behaviour.EMPTY_STRING:
            obj = remove_empty_strings(obj)
        if behaviour & cls.Behaviour.EMPTY_COLLECTIONS:
            obj = remove_empty_collections(obj)
        return obj


class StringFormatter:
    BASIC_ELEMENTS = (str, )

    def __init__(self,
                 mapping: Mapping[str, str | None],
                 track: bool = False,
                 clean_up: CleanUp.Behaviour = CleanUp.Behaviour.EMPTY,
                 format_keys: bool = False,
                 use_provided_mapping: bool = False,
                 # SafeDict settings
                 missing_key: MissingKey.Behaviour = MissingKey.Behaviour.RETURN_PLACEHOLDER,
                 replacement: str | Callable[[str], str | None] | None = MissingKey.DEFAULT,
                 missing_keys_set: MutableSet[str] | None = None,
                 # Parser settings
                 unknown_parser: UnknownParser.Behaviour = UnknownParser.Behaviour.IGNORE,
                 parser_replacement: Any | Callable[[Any], Any | None] | None = UnknownParser.DEFAULT,
                 default_parser: InternalParser | None = None,
                 **parser_kwargs: Any,
                 ):

        # Dictionaries
        if track or missing_keys_set is not None:
            track = True
            dict_cls = partial(SafeDictWrapperWithTracker, missing_keys_set=missing_keys_set)
        else:
            dict_cls = SafeDictWrapper

        if not use_provided_mapping:
            self.mapping = dict_cls(mapping, behaviour=missing_key, replacement=replacement)
        else:
            if track and not isinstance(mapping, SafeDictWrapperWithTracker):
                raise TypeError(f'Tracking is enabled, but the provided mapping is not a '
                                f'{SafeDictWrapperWithTracker.__name__}')
            self.mapping = mapping

        # Parser
        parsing_map = build_parsing_map(element_parser=as_element_parser(safe_format, mapping=self.mapping),
                                        elements=self.BASIC_ELEMENTS)

        self.format = build_parser_from_map(parsing_map,
                                            behaviour=unknown_parser,
                                            replacement=parser_replacement,
                                            wrapper=partial(CleanUp.cleanup, behaviour=clean_up),
                                            default_parser=default_parser,
                                            parse_keys=format_keys,
                                            **parser_kwargs,
                                            )

    @property
    def track(self):
        return isinstance(self.mapping, SafeDictWrapperWithTracker)

    @property
    def missing_keys(self):
        if isinstance(self.mapping, SafeDictWrapperWithTracker):
            return self.mapping.missing_keys
        raise AttributeError(f'{self.__class__.__name__} has not been initialized with track=True')

    def clear_missing_keys(self):
        if isinstance(self.mapping, SafeDictWrapperWithTracker):
            return self.mapping.clear_missing_keys()
        raise AttributeError(f'{self.__class__.__name__} has not been initialized with track=True')


def format_string(obj: Any,
                  mapping: Mapping[str, str | None],
                  missing_key: MissingKey.Behaviour = MissingKey.Behaviour.RETURN_PLACEHOLDER,
                  missing_keys_set: MutableSet[str] | None = None,
                  clean_up: CleanUp.Behaviour = CleanUp.Behaviour.EMPTY,
                  format_keys: bool = False,
                  ):

    formatter = StringFormatter(mapping,
                                clean_up=clean_up,
                                format_keys=format_keys,
                                missing_key=missing_key,
                                missing_keys_set=missing_keys_set,
                                )
    return formatter.format(obj)

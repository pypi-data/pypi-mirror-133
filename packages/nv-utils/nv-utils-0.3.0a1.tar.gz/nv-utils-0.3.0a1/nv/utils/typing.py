"""
Some useful extensions and protocols to standard typing library.
"""

import dataclasses
from typing import Protocol, ClassVar, Any, Dict


class DataClass(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, 'dataclasses.Field']]
    __dataclass_params__: ClassVar[Any]

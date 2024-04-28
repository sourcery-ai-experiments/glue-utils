"""Module for conveniently parsing options resolved from command-line arguments."""

import json
from abc import ABC
from collections.abc import Callable
from dataclasses import Field, dataclass, fields
from typing import Any, TypeVar

from typing_extensions import Self

T = TypeVar("T", dict[str, Any], list[Any])


def _handle_json_field(
    target_type: type[T],
) -> Callable[[Field[T], str], T]:
    def _handle_field(field: Field[T], argument_value: str) -> T:
        value = json.loads(argument_value)
        if not isinstance(value, target_type):
            msg = "Invalid type for %s: %s"
            raise TypeError(msg, field.name, field.type)
        return value

    return _handle_field


_handle_dict_field = _handle_json_field(dict)
_handle_list_field = _handle_json_field(list)


@dataclass(frozen=True)
class BaseOptions(ABC):
    """Abstract base class for storing resolved options."""

    job_name: str

    @classmethod
    def from_resolved_options(
        cls: type[Self],
        resolved_options: dict[str, Any],
    ) -> Self:
        """Create an instance of the class from Glue's resolved options."""
        values: dict[str, Any] = {}

        for field in fields(cls):
            argument_value = resolved_options[field.name.upper()]
            if "dict" in str(field.type):
                values[field.name] = _handle_dict_field(field, argument_value)
            elif "list" in str(field.type):
                values[field.name] = _handle_list_field(field, argument_value)
            elif field.type is bool:
                values[field.name] = bool(json.loads(argument_value))
            else:
                values[field.name] = field.type(argument_value)

        return cls(**values)

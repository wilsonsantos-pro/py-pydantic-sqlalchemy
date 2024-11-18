import datetime
import decimal
import typing
import uuid
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from types import NoneType
from typing import Any, Optional

from pydantic import BaseModel


@dataclass
class ImportDefinition:
    name: str
    package: str = "sqlalchemy"

    def __hash__(self) -> int:
        return hash(self.name + self.package)


_TypeDefinitionDefaults = namedtuple(
    "_TypeDefinitionDefaults",
    "name package args",
    defaults=["sqlalchemy", None],
)


@dataclass
class TypeDefinition:
    type: str
    import_def: ImportDefinition
    nullable: bool = False
    type_args: str | None = None
    compound: bool = False

    @staticmethod
    def get_field_definition(
        field_type: Any, foreign_key: bool = False
    ) -> "TypeDefinition":
        nullable = False
        _type_def = None
        _origin = typing.get_origin(field_type)
        _type_args = None
        compound = False
        if _origin == typing.Union:
            for arg in typing.get_args(field_type):
                if arg == NoneType:
                    nullable = True
                else:
                    _type_def = _type_def_mappings.get(arg)
        elif _origin == list:
            if foreign_key:
                _sub_type = typing.get_args(field_type)[0]
                _type_def = _type_def_mappings.get(_sub_type)
                _type_args = _type_def.args
            else:
                _sub_type = typing.get_args(field_type)[0]
                _type_def = _type_def_mappings.get(_origin)
                _sub_type_def = _type_def_mappings.get(_sub_type)

                if not _type_def:
                    raise ValueError(f"No type def found for {field_type}")

                if not _sub_type_def:
                    raise ValueError(f"No type def found for {_sub_type}")
                _type_args = f"{_sub_type_def.name}, {_type_def.args or ''}"
        elif issubclass(field_type, BaseModel):
            _type_def = _type_def_mappings.get(BaseModel)
            compound = True
        elif issubclass(field_type, Enum):
            _type_def = _type_def_mappings.get(int)
        else:
            _type_def = _type_def_mappings.get(field_type)

        if not _type_def:
            raise ValueError(f"No type def found for {field_type}")

        _type_args = _type_args or _type_def.args

        return TypeDefinition(
            type=_type_def.name,
            import_def=ImportDefinition(_type_def.name, _type_def.package),
            nullable=nullable,
            type_args=_type_args,
            compound=compound,
        )


@dataclass
class Column:
    name: str
    type_definition: TypeDefinition
    related_table: str = ""
    primary_key: Optional[bool] = False
    foreign_key: Optional[bool] = False
    autoincrement: bool = False
    server_default: Optional[Any] = None
    default: Optional[Any] = None
    index: bool = False


@dataclass
class ModelBase:
    """The SQLAlchemy will inherit from this model."""

    name: str = "Base"
    import_def: ImportDefinition = ImportDefinition(
        name="declarative_base", package="sqlalchemy.orm"
    )
    global_def: str = "Base = declarative_base()"


@dataclass
class Relationship:
    name: str
    class_name: str
    related_table: str
    secondary: Optional[str] = None
    back_populates: Optional[str] = None


@dataclass
class Model:
    class_name: str
    model_bases: list[ModelBase]
    table_name: str
    columns: list[Column]
    relationships: list[Relationship]
    is_m2m: bool = False

    @property
    def primary_key(self) -> Column | None:
        for c in self.columns:
            if c.primary_key:
                return c
        return None


_type_def_mappings = {
    int: _TypeDefinitionDefaults(name="Integer"),
    float: _TypeDefinitionDefaults(name="Float"),
    str: _TypeDefinitionDefaults(name="Text"),
    bool: _TypeDefinitionDefaults(name="Boolean"),
    bytes: _TypeDefinitionDefaults(name="LargeBinary"),
    dict: _TypeDefinitionDefaults(
        name="JSONB", package="sqlalchemy.dialects.postgresql"
    ),
    list: _TypeDefinitionDefaults(
        name="ARRAY", package="sqlalchemy.dialects.postgresql", args="dimensions=1"
    ),
    Enum: _TypeDefinitionDefaults(name="Integer"),
    datetime.datetime: _TypeDefinitionDefaults(name="DateTime"),
    datetime.date: _TypeDefinitionDefaults(name="Date"),
    datetime.time: _TypeDefinitionDefaults(name="Time"),
    decimal.Decimal: _TypeDefinitionDefaults(name="Numeric"),
    uuid.UUID: _TypeDefinitionDefaults(
        name="UUID", package="sqlalchemy.dialects.postgresql", args="as_uuid=True"
    ),
    BaseModel: _TypeDefinitionDefaults(
        name="JSONB", package="sqlalchemy.dialects.postgresql"
    ),
}

import typing
from dataclasses import dataclass, field

from pydantic import BaseModel

from .model import (
    Column,
    ImportDefinition,
    Model,
    ModelBase,
    Relationship,
    TypeDefinition,
)
from .utils import camel_to_snake, snake_to_camel


@dataclass
class ParseResult:
    models: list[Model]
    imports: list[ImportDefinition]
    global_defs: list[str]


def _default_model_bases_factory():
    return [ModelBase()]


@dataclass
class ParserConfig:
    model_bases: list[ModelBase] = field(default_factory=_default_model_bases_factory)


def parse_pydantic_model(
    pydantic_model: typing.Type[BaseModel], parser_config: ParserConfig | None = None
) -> ParseResult:
    return _PydanticModelParser(pydantic_model, parser_config or ParserConfig()).parse()


M2M_SUFFIX = "assoc"


@dataclass
class _PydanticModelParser:
    pydantic_model: typing.Type[BaseModel]
    parser_config: ParserConfig
    columns: list[Column] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    models: list[Model] = field(default_factory=list)
    table_name: str = ""
    imports: set[ImportDefinition] = field(default_factory=set)
    base: ModelBase = field(default_factory=ModelBase)

    def __post_init__(self):
        self.table_name = camel_to_snake(self.pydantic_model.__name__)

    def parse(self) -> ParseResult:

        for field_name, field_type in self.pydantic_model.__annotations__.items():
            _field_definition = TypeDefinition.get_field_definition(field_type)
            self.imports.add(_field_definition.import_def)

            if field_name.endswith("_id"):
                # Foreign key field
                related_table = field_name[:-3].capitalize()
                _field_definition = TypeDefinition.get_field_definition(
                    field_type, foreign_key=True
                )
                class_name = camel_to_snake(related_table)
                self.columns.append(
                    Column(
                        name=field_name,
                        type_definition=_field_definition,
                        foreign_key=True,
                        related_table=related_table,
                    )
                )
                self.relationships.append(
                    Relationship(
                        class_name=class_name,
                        name=field_name[:-3].lower(),
                        related_table=related_table,
                    )
                )

            elif field_name.endswith("_ids") and typing.get_origin(field_type) == list:
                # Many-to-Many relationship
                related_table = field_name[:-4]
                m2m_class_name = snake_to_camel(
                    f"{self.table_name}_{related_table}_{M2M_SUFFIX}"
                )
                m2m_table_name = f"{camel_to_snake(m2m_class_name)}"
                _field_definition = TypeDefinition.get_field_definition(
                    field_type, foreign_key=True
                )
                m2m_table_columns = [
                    Column(
                        name=f"{self.table_name}_id",
                        type_definition=_field_definition,
                        primary_key=True,
                        foreign_key=True,
                        related_table=self.table_name,
                    ),
                    Column(
                        name=f"{related_table}_id",
                        type_definition=_field_definition,
                        primary_key=True,
                        foreign_key=True,
                        related_table=related_table,
                    ),
                ]

                self.models.append(
                    Model(
                        class_name=m2m_class_name,
                        model_bases=self.parser_config.model_bases,
                        table_name=m2m_table_name,
                        columns=m2m_table_columns,
                        relationships=[],
                        is_m2m=True,
                    )
                )

                # Define the relationship for the many-to-many association
                self.relationships.append(
                    Relationship(
                        class_name=m2m_class_name,
                        name=related_table.lower() + "s",
                        related_table=related_table,
                        secondary=m2m_table_name.lower(),
                        back_populates=self.table_name.lower(),
                    )
                )
            else:
                if _field_definition.compound:
                    _parse_result = _PydanticModelParser(
                        field_type, self.parser_config
                    ).parse()
                    if (
                        _parse_result.models
                        and (_primary_key := _parse_result.models[0].primary_key)
                        is not None
                    ):
                        self.columns.append(
                            Column(
                                name=f"{field_name}_id",
                                type_definition=_primary_key.type_definition,
                            )
                        )
                        continue

                # Basic types
                self.columns.append(
                    Column(
                        name=field_name,
                        type_definition=_field_definition,
                        primary_key=field_name == "id",
                    )
                )

        model = Model(
            class_name=self.pydantic_model.__name__,
            model_bases=self.parser_config.model_bases,
            table_name=self.table_name,
            columns=self.columns,
            relationships=self.relationships,
        )
        self.models.insert(0, model)

        if self.relationships:
            self.imports.add(ImportDefinition(name="ForeignKey"))

        self.imports.add(ImportDefinition(name="Column"))

        globals_defs = set()
        for m in self.models:
            for b in m.model_bases:
                self.imports.add(b.import_def)
                globals_defs.add(b.global_def)

        return ParseResult(
            models=self.models if model.primary_key else [],
            imports=list(self.imports),
            global_defs=list(globals_defs),
        )

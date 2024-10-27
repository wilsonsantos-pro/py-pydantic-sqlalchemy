from dataclasses import dataclass
from typing import List, Optional, Type

from pydantic import BaseModel


@dataclass
class SqlAlchemyColumn:
    name: str
    type: str
    primary_key: bool
    nullable: bool


@dataclass
class SqlAlchemyModel:
    parent: str
    table_name: str
    columns: List[SqlAlchemyColumn]

    def to_str(self) -> str:
        code_str = f"class {self.table_name.capitalize()}(Base):\n"
        code_str += f'    __tablename__ = "{self.table_name}"\n'
        for column in self.columns:
            extra_kwargs = ""
            if column.primary_key:
                extra_kwargs += ", primary_key=True"
            if column.nullable:
                extra_kwargs += ", nullable=True"
            else:
                extra_kwargs += ", nullable=False"
            code_str += f"    {column.name} = Column({column.type}{extra_kwargs})\n"
        return code_str


def pydantic_to_sqlalchemy_code(
    pydantic_model: Type[BaseModel], table_name: str
) -> str:
    columns = []

    for field_name, field_type in pydantic_model.__annotations__.items():
        if field_type == int:
            columns.append(
                SqlAlchemyColumn(
                    name=field_name,
                    type="Integer",
                    primary_key=field_name == "id",
                    nullable=False,
                ),
            )
        elif field_type == str:
            columns.append(
                SqlAlchemyColumn(
                    name=field_name,
                    type="Text",
                    primary_key=False,
                    nullable=False,
                ),
            )
        elif field_type == Optional[int]:
            columns.append(
                SqlAlchemyColumn(
                    name=field_name,
                    type="Integer",
                    primary_key=False,
                    nullable=True,
                ),
            )

    sqlalchemy_model = SqlAlchemyModel(
        parent="Base", table_name=table_name, columns=columns
    )
    return sqlalchemy_model.to_str()

from typing import Optional, Type

from pydantic import BaseModel


def pydantic_to_sqlalchemy_code(
    pydantic_model: Type[BaseModel], table_name: str
) -> str:
    code_str = f"class {table_name.capitalize()}(Base):\n"
    code_str += f'    __tablename__ = "{table_name}"\n'

    for field_name, field_type in pydantic_model.__annotations__.items():
        if field_type == int:
            code_str += f'    {field_name} = Column(Integer, primary_key={field_name == "id"})\n'
        elif field_type == str:
            code_str += f"    {field_name} = Column(Text)\n"
        elif field_type == Optional[int]:
            code_str += f"    {field_name} = Column(Integer, nullable=True)\n"

    return code_str

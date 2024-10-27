from typing import Optional

from pydantic import BaseModel

from py_pydantic_sqlalchemy.generator import pydantic_to_sqlalchemy_code


class User(BaseModel):
    id: int
    name: str
    age: Optional[int]


def test_pydantic_to_sqlalchemy_code():
    expected = """class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer, nullable=True)
"""
    assert pydantic_to_sqlalchemy_code(User, "user") == expected

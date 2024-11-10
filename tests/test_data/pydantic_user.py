from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    postal_code: int
    city: str


class Parent:
    id: int
    name: str


class User(BaseModel):
    id: int
    name: str
    age: Optional[int]
    address_id: int
    parent_ids: list[int]

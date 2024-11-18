import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    id: uuid.UUID
    postal_code: int
    city: str


class Parent(BaseModel):
    id: int
    name: str


class Account(BaseModel):
    id: int
    name: str


class Preferences(BaseModel):
    color: str
    days: int


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    YELLOW = "yellow"


class User(BaseModel):
    id: int
    name: str
    age: Optional[int]
    account_id: int
    address_ids: list[uuid.UUID]
    parent_ids: list[int]
    interests: list[str]
    favorite_numbers: list[int]
    preferences: Preferences
    main_address: Address
    favorite_color: Color

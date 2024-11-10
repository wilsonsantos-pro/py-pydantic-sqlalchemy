from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = "address"

    postal_code = Column(Integer, nullable=False)
    city = Column(Text, nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)


class UserParentAssoc(Base):
    __tablename__ = "user_parent_assoc"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("parent.id"), primary_key=True, nullable=False
    )

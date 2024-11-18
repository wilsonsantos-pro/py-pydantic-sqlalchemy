from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, nullable=False)
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


def insert_address(session, data: dict[str, Any]) -> None:
    record = Address(
        id=data["id"],
        postal_code=data["postal_code"],
        city=data["city"],
    )
    session.add(record)


def insert_user(session, data: dict[str, Any]) -> None:
    record = User(
        id=data["id"],
        name=data["name"],
        age=data.get("age"),
        address_id=data["address_id"],
    )
    session.add(record)

    parent_ids = data.get("parent_ids", [])
    for related_record_id in parent_ids:
        related_record = UserParentAssoc(
            user_id=data["id"], parent_id=related_record_id
        )
        session.add(related_record)

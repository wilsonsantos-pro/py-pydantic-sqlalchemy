from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)


class Address(Base):
    __tablename__ = "address"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    postal_code = Column(Integer, nullable=False)
    city = Column(Text, nullable=False)


class Parent(Base):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    interests = Column(ARRAY(Text, dimensions=1), nullable=False)
    favorite_numbers = Column(ARRAY(Integer, dimensions=1), nullable=False)
    preferences = Column(JSONB, nullable=False)
    main_address_id = Column(UUID(as_uuid=True), nullable=False)
    favorite_color = Column(Integer, nullable=False)


class UserAddressAssoc(Base):
    __tablename__ = "user_address_assoc"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True, nullable=False
    )
    address_id = Column(
        UUID(as_uuid=True), ForeignKey("address.id"), primary_key=True, nullable=False
    )


class UserParentAssoc(Base):
    __tablename__ = "user_parent_assoc"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("parent.id"), primary_key=True, nullable=False
    )


def insert_account(session, data: dict[str, Any]) -> None:
    record = Account(
        id=data["id"],
        name=data["name"],
    )
    session.add(record)


def insert_address(session, data: dict[str, Any]) -> None:
    record = Address(
        id=data["id"],
        postal_code=data["postal_code"],
        city=data["city"],
    )
    session.add(record)


def insert_parent(session, data: dict[str, Any]) -> None:
    record = Parent(
        id=data["id"],
        name=data["name"],
    )
    session.add(record)


def insert_user(session, data: dict[str, Any]) -> None:
    record = User(
        id=data["id"],
        name=data["name"],
        age=data.get("age"),
        account_id=data["account_id"],
        interests=data["interests"],
        favorite_numbers=data["favorite_numbers"],
        preferences=data["preferences"],
        main_address_id=data["main_address_id"],
        favorite_color=data["favorite_color"],
    )
    session.add(record)

    address_ids = data.get("address_ids", [])
    for related_record_id in address_ids:
        related_record = UserAddressAssoc(
            user_id=data["id"], address_id=related_record_id
        )
        session.add(related_record)

    parent_ids = data.get("parent_ids", [])
    for related_record_id in parent_ids:
        related_record = UserParentAssoc(
            user_id=data["id"], parent_id=related_record_id
        )
        session.add(related_record)

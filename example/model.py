import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from orm_query_api.services.db_services import Base
from orm_query_api.services.serialization import BaseSerializer, SerializerField, RelationField


class ToDo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    priority: Mapped[int] = mapped_column(Integer)
    is_main: Mapped[bool] = mapped_column(Boolean)
    worker_fullname: Mapped[str] = mapped_column(String)
    due_date: Mapped[datetime.date] = mapped_column(Date)
    count: Mapped[int] = mapped_column(Integer, default=1)
    users: Mapped[List["User"]] = relationship(
        secondary="todo_user", back_populates="todos"
    )


class ToDoPydantic(BaseModel):
    comment: str | None = None
    created_at: datetime.datetime
    priority: int
    is_main: bool = False
    worker_fullname: str
    due_date: datetime.date
    count: int = 0
    user_ids: List[int]


class ToDoSerializer(BaseSerializer):
    model = ToDo
    fields = [
        SerializerField("id", "primary_key"),
        SerializerField("comment", "instruction"),
        SerializerField("created_at", "creation_time"),
        SerializerField("priority", "preference"),
        SerializerField("is_main", "is_principal"),
        SerializerField("worker_fullname", "worker"),
        SerializerField("due_date", "deadline"),
        SerializerField("count", "amount"),
        RelationField("slaves", "slaves"),
        RelationField("users", "users"),
    ]


class ToDoSlave(Base):
    __tablename__ = "todoslave"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    todo_id: Mapped[int] = mapped_column(ForeignKey("todo.id"))
    todo = relationship("ToDo", backref="slaves", lazy=True)
    slavedetails = relationship('ToDoSlaveDetails', uselist=False, back_populates='todo_slave')


class ToDoSlavePydantic(BaseModel):
    comment: str | None = None
    created_at: datetime.datetime
    todo_id: int | None = None


class ToDoSlaveSerializer(BaseSerializer):
    model = ToDoSlave
    fields = [
        SerializerField("id", "primary_key"),
        SerializerField("comment", "instruction"),
        SerializerField("created_at", "creation_time"),
        RelationField("todo", "todo"),
        RelationField("slavedetails", "slavedetails"),
    ]


class ToDoSlaveDetails(Base):
    __tablename__ = "todoslavedetails"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    details: Mapped[str] = mapped_column(String, nullable=True, default=None)

    todo_slave_id = mapped_column(Integer, ForeignKey("todoslave.id"))
    todo_slave = relationship("ToDoSlave", back_populates="slavedetails")


class ToDoSlaveDetailsPydantic(BaseModel):
    details: str | None = None
    todo_slave_id: int | None = None


class ToDoSlaveDetailsSerializer(BaseSerializer):
    model = ToDoSlaveDetails
    fields = [
        SerializerField("id", "primary_key"),
        SerializerField("details", "info"),
    ]


class TodoUser(Base):
    __tablename__ = "todo_user"
    todo_id: Mapped[int] = mapped_column(ForeignKey("todo.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    todo: Mapped["ToDo"] = relationship("ToDo")
    user: Mapped["User"] = relationship("User")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String)
    date_birth: Mapped[datetime.date] = mapped_column(Date)
    city: Mapped[str] = mapped_column(String)
    todos: Mapped[List["ToDo"]] = relationship(
        secondary="todo_user", back_populates="users"
    )


class UserPydantic(BaseModel):
    fullname: str
    date_birth: datetime.date
    city: str
    todo_ids: List[int]


class UserSerializer(BaseSerializer):
    model = User
    fields = [
        SerializerField("id", "primary_key"),
        SerializerField("fullname", "fullname"),
        SerializerField("date_birth", "date_birth"),
        SerializerField("city", "city"),
        RelationField("todos", "todos"),
    ]

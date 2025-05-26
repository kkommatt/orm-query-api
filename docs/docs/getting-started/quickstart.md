### Quick Start

Below is a simple example of how to go from a SQLAlchemy model to a running API endpoint:

1. **Define your SQLAlchemy model** (using any declarative base). For example:

   ```python
   import datetime
   from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Date
   from sqlalchemy.orm import Mapped, relationship
   from orm_query_api.services.db_services import Base  # SQLAlchemy Base
   from typing import List

   class ToDo(Base):
       __tablename__ = "todo"
       id: Mapped[int] = Column(Integer, primary_key=True)
       comment: Mapped[str] = Column(String, nullable=True, default=None)
       created_at: Mapped[datetime.datetime] = Column(
           DateTime(timezone=True), server_default=func.now()
       )
       priority: Mapped[int] = Column(Integer)
       is_main: Mapped[bool] = Column(Boolean)
       worker_fullname: Mapped[str] = Column(String)
       due_date: Mapped[datetime.date] = Column(Date)
       count: Mapped[int] = Column(Integer, default=1)
       users: Mapped[List["User"]] = relationship(
           secondary="todo_user", back_populates="todos"
       )
   ```

2. **Define a Pydantic schema and serializer**.  The Pydantic `BaseModel` is used for input validation (`POST`/`PUT`), while a `BaseSerializer` subclass lists the fields (and any nested relations) for output.  For example:

   ```python
   from pydantic import BaseModel
   import datetime
   from typing import List
   from orm_query_api.services.serialization import BaseSerializer, SerializerField, RelationField

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
           RelationField("users", "users"),
       ]
   ```

   In this serializer, we assign custom aliases like `"primary_key"` for `id` or `"deadline"` for `due_date`, which will be the JSON keys in responses.  The `RelationField` indicates a relationship to include (e.g. `users`).

3. **Generate and include the router**.  Use `generate_crud_router` to create a FastAPI `APIRouter` with CRUD endpoints for your model.  For example:

   ```python
   from fastapi import FastAPI
   from orm_query_api.routes import generate_crud_router

   app = FastAPI()

   todo_router = generate_crud_router(
       model=ToDo,
       serializer=ToDoSerializer,
       pydantic_model=ToDoPydantic,
       prefix="todo"
   )
   app.include_router(todo_router)
   ```

   This creates endpoints like `GET /todo/`, `GET /todo/{id}`, `POST /todo/`, etc. The `q=` query-string syntax (shown below) can then be used on the list endpoint.

With these steps, you have a working API: for example, `GET /todo/` will list ToDo items, and you can filter or sort them by using queries like `GET /todo/?q=(id,created_at).filter(created_at>=2023-01-01).order(created_at,desc)`.

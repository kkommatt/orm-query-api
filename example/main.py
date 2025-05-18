import uvicorn
from fastapi import FastAPI

from model import ToDo, ToDoPydantic, ToDoSerializer, ToDoSlave, ToDoSlaveSerializer, ToDoSlavePydantic, \
    ToDoSlaveDetails, \
    ToDoSlaveDetailsSerializer, ToDoSlaveDetailsPydantic, User, UserSerializer, UserPydantic
from orm_query_api.registry import model_registry
from orm_query_api.services.db_services import init_db
from orm_query_api.services.exc_handlers import register_exception_handlers
from orm_query_api.utils.auto_gen import create_schema_and_serializer

app = FastAPI()
init_db()
# pydantic_model, serializer_model = create_schema_and_serializer(ToDo)

model_registry.register_model(ToDo, serializer_class=ToDoSerializer, pydantic_model=ToDoPydantic)

model_registry.register_model(ToDoSlave, serializer_class=ToDoSlaveSerializer, pydantic_model=ToDoSlavePydantic)

model_registry.register_model(ToDoSlaveDetails, serializer_class=ToDoSlaveDetailsSerializer,
                              pydantic_model=ToDoSlaveDetailsPydantic)

model_registry.register_model(User, serializer_class=UserSerializer, pydantic_model=UserPydantic)

model_registry.register_all_routes(app)

register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(app)

## Usage

### Registering Models

There are two main ways to register models and set up routes:

* **Using `generate_crud_router` directly**: As shown above, call `generate_crud_router(model, serializer, pydantic_model, prefix)` and include the returned router in your app. This is good for a few models or manual control.

* **Using `ModelRegistry`**: The `ModelRegistry` class lets you register multiple models and then include all routes at once. Example:

  ```python
  from orm_query_api.registry import ModelRegistry
  from fastapi import FastAPI

  app = FastAPI()
  registry = ModelRegistry()

  # Register a model; serializer and schema will be auto-generated if omitted
  registry.register_model(model=ToDo, serializer_class=ToDoSerializer, pydantic_model=ToDoPydantic)
  registry.register_all_routes(app)
  ```

  Internally, `register_model` stores the model info and calls `generate_crud_router` with that model's info. You can supply a custom `prefix` or let it default to the lowercase model name. If you omit `serializer_class` or `pydantic_model`, the library can auto-generate a Pydantic schema and serializer using all model columns.

* **Advanced options**: When registering, you can pass a custom URL prefix (e.g. `prefix="tasks"`) or a custom serializer. If `auto_generate=True` in `register_model`, it will ignore provided `serializer_class` and create fresh ones.  By default, the router includes all standard CRUD endpoints (list, retrieve, create, update, partial update, delete).

Regardless of approach, the generated **list endpoint** (e.g. `GET /todo/`) automatically uses the `q=` query parameter: it calls `parse_query()`, validates with your serializer, then runs `get_all()` to return JSON data.

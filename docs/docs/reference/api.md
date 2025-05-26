
## Reference

### ModelRegistry

```python
class ModelRegistry:
    registry: Dict[str, Dict]
    router: APIRouter
```

The **ModelRegistry** class helps you register multiple models at once. Key methods:

* `register_model(model, serializer_class=None, prefix=None, pydantic_model=None, auto_generate=False)`: Registers a model. If no `serializer_class` or `pydantic_model` is provided (or if `auto_generate=True`), the library auto-generates them via `create_schema_and_serializer`. The model is stored in `registry`, and an `APIRouter` is created with CRUD endpoints for that model (using `generate_crud_router`).
* `register_all_routes(app: FastAPI)`: Includes the combined router into the given FastAPI app (i.e. `app.include_router(self.router)`).

Internally, `ModelRegistry` maintains a single FastAPI `APIRouter` (in `self.router`) and merges each generated router into it.

### generate\_crud\_router

```python
def generate_crud_router(model: Type, serializer: Type[BaseSerializer], prefix: str, pydantic_model: Type[BaseModel]) -> APIRouter
```

The **generate\_crud\_router** function returns a FastAPI `APIRouter` for a given SQLAlchemy model. It creates the following endpoints under `/{prefix}`:

* `GET /` – List items, using `q=` for filtering/sorting.
* `GET /{item_id}` – Retrieve a single item by primary key (raises 404 if not found).
* `POST /` – Create a new item, expecting a Pydantic body; commits to DB.
* `PUT /{item_id}` – Replace an item (404 if not exists).
* `PATCH /{item_id}` – Update an item partially (only provided fields).
* `DELETE /{item_id}` – Delete an item (returns 204 on success).

The list endpoint (`GET /`) uses `parse_query()` and `validate_query_options()` to apply the requested filters/sorting, then runs `get_all()` to return JSON.

### parse\_query

```python
def parse_query(q: str) -> ActionTree
```

Parses a raw query string (the part after `q=`) into an `ActionTree`. The grammar is LALR-based; `parse_query` wraps the Lark parser and transforms syntax errors into a `ValidationException`. For example, `parse_query("(id,name).filter(age>=30)")` returns an `ActionTree` with `select=["id","name"]` and a filter on `age`. Malformed queries will raise an exception with an error message.

### BaseSerializer

```python
class BaseSerializer:
    model: Any
    fields: List[SerializerField]
```

To customize serialization, define a subclass of `BaseSerializer` for your model. Key points:

* `model`: the SQLAlchemy model class this serializer is for.
* `fields`: a list of `SerializerField` (or `RelationField`) objects defining which fields to output and their aliases.
* `get_model_inspection()`: Returns SQLAlchemy metadata inspector for the model.
* `get_db_field(db_field: str)`: Look up the actual `InstrumentedAttribute` (column) for a given field name.
* `get_serializer_field(field_alias: str)`: Find the `SerializerField` by alias.
* **Automatic registration:** When you subclass `BaseSerializer`, it automatically registers itself in an internal registry (used by `get_serializer()`).

### SerializerField and RelationField

```python
class SerializerField:
    def __init__(self, field: str, alias: Optional[str], type_: Optional[type] = None)
```

A **SerializerField** represents a single model field.

* `field`: the actual attribute name on the SQLAlchemy model.
* `alias`: (optional) the name to use in JSON output (defaults to the same as `field` if not provided).
* `type_`: (optional) Python type of the field (not usually needed).

```python
class RelationField(SerializerField):
    ...
```

A **RelationField** is used for relationship fields (e.g. a `relationship` on the SQLAlchemy model). Use it in `fields` to include related objects. For example, `RelationField("users", "users")` indicates including the `users` relation.

Other utility functions:

* `get_serializer(model_type)`: Returns the serializer class registered for a given model.
* `get_prop_serializer(model_type, prop_name)`: Given a model and a relationship property name, returns the serializer for the related model.

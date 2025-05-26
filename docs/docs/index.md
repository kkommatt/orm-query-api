# ORM Query API

**orm-query-api** is a modern Python library for dynamically generating RESTful CRUD APIs from SQLAlchemy ORM models using FastAPI — complete with advanced query parsing, validation, and automatic serialization.  Its philosophy is to minimize boilerplate by providing a high-level interface that **auto-generates routers** and parses complex URI query strings, translating them into SQL expressions under the hood.  Developers define their models and (optionally) serializers once, and the library handles CRUD endpoints, query filtering, sorting, pagination, and nested relationships automatically.

Core concepts include:

* **Auto-generated routers**: Create CRUD endpoints (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) for any SQLAlchemy model with one function call or via a central registry.
* **Query-string syntax**: Use a formal Lark-based grammar to filter, sort, offset, and limit results via a single `q=` parameter.
* **Serialization**: Define custom serializers (with `SerializerField`/`RelationField`) to control output names and nested relationships; by default, serializers can be auto-generated from models.
* **Validation**: Query parameters are parsed into an `ActionTree` (holding select fields, filters, sort, etc.) and validated against the serializer so that invalid fields or operators are caught before SQL execution.

**Features at a glance** include:

* ✅ Auto-generate CRUD endpoints for any SQLAlchemy model
* ✅ Support for query-string filters, sorting, pagination, and nested relations
* ✅ Typed input via Pydantic models (for `POST`/`PUT`/`PATCH`)
* ✅ Response serialization using customizable serializers (with field aliasing)
* ✅ Built-in query parsing (via Lark) and validation of fields/operators
* ✅ Easily composable into any FastAPI app (just include the generated routers)

Together, these features let you focus on your data model and business logic, while **orm-query-api** handles the repetitive REST API wiring and query logic for you.
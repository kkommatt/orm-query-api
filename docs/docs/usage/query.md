### Querying with `q=` Syntax

The library supports a powerful URI query syntax using a single `q` parameter. A typical query looks like:

```
GET /todo/?q=(id,priority,users).filter(priority>=5,user_fullname="Alice").order(created_at,asc).offset(10).limit(5)
```

This breaks down as follows:

* **Selection (`(...)`)**: Inside the parentheses you list fields to select. You can use `*` for all fields or prefixes like `!` to exclude (e.g. `!password`). You can also select nested relations, e.g. `users(id,name)` to include related users with only `id` and `name`.

* **Filtering (`.filter(fieldOPvalue)`)**: Append `.filter(...)` with conditions. Supported operators include `=`, `!=`, `>`, `<`, `>=`, `<=`, `in`, `is_null`, `like`, and `ilike`. For example, `.filter(priority>=5)` or `.filter(user_fullname="Alice")`. You can filter on nested fields using dot syntax: e.g. `.filter(users.id=2)` filters todos whose related user has ID 2.

* **Sorting (`.order(field,asc|desc)`)**: Use `.order(field,asc)` or `.order(field,desc)` to sort the results. E.g. `.order(created_at,desc)` for newest first.

* **Pagination (`.offset()` and `.limit()`)**: Use `.offset(N)` to skip `N` records and `.limit(N)` to restrict the number of results.

The grammar (defined in code) enforces this structure. Under the hood, `parse_query(q_str)` (in `orm_query_api/parser/query_parser.py`) parses the string into an `ActionTree` object. This tree has attributes: `select` (list of fields or nested field specifiers), `filters` (list of `FilterAction`), `sort` (`SortAction`), `offset` (int), `limit` (int), and `relations` (a dict of nested `ActionTree` for related models). For example:

* Given `q=(id,name,users(id,name)).filter(users.id=5,priority>=10).order(name,asc).limit(20)`, the parser builds an `ActionTree` where:

  * `select = ["id", "name", "users"]` (with `users` having its own ActionTree specifying `select=["id","name"]` internally).
  * `filters = [ FilterAction(field=NestedField(["users","id"]), operator=InstrumentedAttribute.eq, value=5), FilterAction(field="priority", operator=operator.ge, value=10) ]`.
  * `sort = SortAction(field=NestedField(["name"]), order=SortOrder.ASC)`.
  * `limit = 20`, `offset = None` (default 0).

Each `FilterAction` holds a `field` (possibly nested, e.g. `NestedField(["users","id"])`), an SQLAlchemy operator function (e.g. `operator.eq` for `=`), and the value. The library then translates this `ActionTree` into an actual SQLAlchemy query (via `get_all()`), including joins for any nested relations.

**Examples:**

1. Filter and sort example:

   ```
   GET /todo/?q=(id,priority).filter(priority>=5,worker_fullname="Alice").order(created_at,desc)
   ```

   * Selects only `id` and `priority` fields of `ToDo`.
   * Filters `priority >= 5` **AND** `worker_fullname = "Alice"`.
   * Sorts by `created_at` descending.

2. Nested query example:

   ```
   GET /todo/?q=(id,comment,users(id,name)).filter(users.id=3).offset(10).limit(5)
   ```

   * Selects `id`, `comment`, and a nested `users` relation with only `id` and `name`.
   * Filters where a related `users.id` equals 3.
   * Applies pagination (skip 10, take 5).

The `parse_query` and subsequent validation ensure that only known fields (as defined in your serializer) and supported operators are used. Invalid syntax or unknown fields will raise a `ValidationException`.

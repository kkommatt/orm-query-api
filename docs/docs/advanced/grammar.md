### Query Grammar and Parser

The formal grammar for the `q` parameter is defined in \[**`orm_query_api/parser/query_parser.py`**], using Lark:

```
start: "q" "=" action_tree

action_tree: "(" field ("," field)* ")" 
             ("." filter_fn)? ("." offset_fn)? ("." limit_fn)? ("." order_fn)?

filter_fn: "filter" "(" nested_field FILTER_OP rvalue ")"
order_fn: "order" "(" nested_field "," SORT_ORDER ")"
limit_fn: "limit" "(" NUMBER ")"
offset_fn: "offset" "(" NUMBER ")"

!field: "!" CNAME | CNAME | "*" | relation
nested_field: CNAME ("." CNAME)*
relation: CNAME action_tree
```

* **Fields**: `field` can be a simple column name, `*` (wildcard), a negation like `!password` (to exclude), or a relation.
* **Nested fields**: `nested_field` allows things like `user.address.city`.
* **filter\_fn**: Filters take the form `filter(fieldOPvalue)`, e.g. `filter(age>=30)`, `filter(name="Alice")`.
* **order\_fn**: Sorting like `order(created_at,desc)`.
* **offset/limit**: Simple numeric pagination.

The parser (via `SelectQueryTransformer`) builds an `ActionTree` where each part of the query string populates fields, filters, sort, etc. To extend or modify the grammar, you could edit this Lark grammar string or wrap the transformer. For example, you could add new functions (like `search(...)`) by modifying the grammar and transformer in `query_parser.py`.

Internally, once parsed, the `ActionTree` is validated in `orm_query_api/parser/query_validation.py` to ensure all referenced fields actually exist in the serializer, and then turned into SQL in `orm_query_api/parser/query_parse.py`. The library relies on standard JSON aggregation functions (`group_concat`, `json`, etc.) in SQL to return result sets as JSON arrays.

A helpful debugging tip is that if you supply an invalid query string, `parse_query` will throw a `ValidationException` with a Lark error message, telling you where the syntax failed.

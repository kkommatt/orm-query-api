
## Advanced

### Custom Serializers and Field Aliasing

You can fully customize how model fields appear in your API by writing your own serializer:

* **Field aliasing**: In `SerializerField("db_field", "alias")`, the second argument is the key used in JSON. For example, `SerializerField("created_at", "creation_time")` means the API will return `"creation_time": "2023-01-01T..."` rather than `"created_at"`.
* **Excluding fields**: Simply omit a field from `fields` to exclude it. (You can also exclude dynamically via the `!field` syntax in the query string, which inverts selection.)
* **Nested relations**: Use `RelationField("relation_name", "alias")` and then query with e.g. `relation_name(id,name)` to retrieve sub-objects.

Example of chaining serializers (using one serializer inside another) might be accomplished by manually invoking `get_serializer()` inside a custom serialize method, but the library’s focus is on flat definitions of fields. If you need custom logic (e.g. computed fields), you can simply compute them in your Pydantic models or in FastAPI endpoint logic; **orm-query-api** is primarily about wiring existing model fields.

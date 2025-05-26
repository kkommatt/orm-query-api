## FAQ

**Q: How does performance scale with complex queries?**
A: **orm-query-api** constructs SQL queries that use JSON aggregation for nested relations. For simple queries, performance is comparable to writing equivalent SQLAlchemy queries by hand. However, deeply nested or very large result sets may be slower due to JSON construction (`group_concat` or similar). In practice, this is often acceptable for typical REST API use-cases, but be mindful of large data loads. There is no inherent caching or asynchronous DB layer, so consider database indexing and pagination for large tables.

**Q: Does it support async or SQLModel?**
A: Currently, the library is written around **SQLAlchemy’s synchronous ORM**. The generated endpoints are defined as `async def`, but they use a synchronous session (`session = get_session()`) under the hood. True async SQL support (e.g. with an async engine or SQLModel) is on the roadmap. For now, if you need async, you would have to integrate your own async session management or wait for future versions.

**Q: Can I use SQLModel classes?**
A: **SQLModel** is built on top of SQLAlchemy, so in principle you could wrap a SQLModel in this library by treating it like a SQLAlchemy model. However, direct compatibility isn’t officially provided yet. The roadmap mentions SQLModel compatibility as a planned feature. For now, you’d need to ensure your SQLModel behaves like a SQLAlchemy Declarative model (i.e. having a `__table__` and relationships) and possibly write a custom serializer for it.

**Q: How do I debug a malformed `q=` query?**
A: If the `q` parameter has a syntax error or refers to unknown fields, the library will raise a `ValidationException` with details. For example, a missing parenthesis or unknown operator will trigger Lark to complain. Ensure your query matches the grammar (e.g. quotes around strings, proper commas, valid field names). Logging the exception message will usually point to the problem location in the query string.

**Q: What about filtering on related models?**
A: You can filter on nested relationships using dot syntax. For example, if `ToDo` has a relationship `user`, you could do `.filter(user.id=10)` or `.filter(user.name="Alice")`. Internally, this causes a JOIN on the related table. Just ensure you included the relation in the select part (or use `users(id,name)` in the select) if you want to see those fields in the response.

These FAQs cover common concerns. For any other questions, remember that **orm-query-api** is open-source (MIT license) and contributions are welcome. The library’s [GitHub repository](https://github.com/kkommatt/orm-query-api) contains more examples, issue tracking, and an evolving roadmap.

```sh
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"resource": "/", "path": "/", "httpMethod": "GET", "requestContext": {}, "multiValueQueryStringParameters": null}'

```

```json
{
  "resource": "/",
  "path": "/",
  "httpMethod": "GET",
  "requestContext": {}
}
```

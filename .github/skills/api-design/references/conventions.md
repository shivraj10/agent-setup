# URL Naming Conventions

```
GET    /donors                    # list (with filtering + pagination)
GET    /donors/{donor_id}         # get one
POST   /donors                    # create
PUT    /donors/{donor_id}         # full update
PATCH  /donors/{donor_id}         # partial update
DELETE /donors/{donor_id}         # delete

GET    /donors/{donor_id}/deferrals   # nested resource
POST   /donors/{donor_id}/deferrals   # create nested
```

## Rules
- Plural nouns: `/donors` not `/donor`
- Lowercase with hyphens: `/donor-journeys` not `/donorJourneys`
- No verbs in URLs: `/donors` not `/getDonors`
- Nest max 2 levels deep

# Status Codes

| Code | When |
|---|---|
| `200 OK` | GET success, PUT/PATCH success |
| `201 Created` | POST success (include `Location` header) |
| `204 No Content` | DELETE success |
| `400 Bad Request` | Validation error (include details) |
| `401 Unauthorized` | Missing or invalid auth token |
| `403 Forbidden` | Valid token but insufficient permissions |
| `404 Not Found` | Resource doesn't exist |
| `409 Conflict` | Duplicate / state conflict |
| `422 Unprocessable Entity` | Structurally valid but semantically wrong |
| `429 Too Many Requests` | Rate limited |
| `500 Internal Server Error` | Unexpected failure (never expose internals) |

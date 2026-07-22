# BE-W3-A3-Containerize-your-stack
## W3 A3 Repo

# Containerized Task API

A FastAPI task CRUD service running against a PostgreSQL database containerized with Docker Compose.

---

## Quick Start (One Command)

1. Clone the repository:
   ```bash
   git clone [https://github.com/childofparents/BE-W3-A3-Containerize-your-stack.git](https://github.com/childofparents/BE-W3-A3-Containerize-your-stack.git)
   cd BE-W3-A3-Containerize-your-stack
   ```

2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

3. Start the entire stack:
   ```bash
   docker compose up --build
   ```

The app will start at `http://localhost:8000` with the database pre-seeded with 3 initial tasks.

---

## Standalone Postgres Docker Command (Stage 0)

To run only the standalone Postgres container:
```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
```

---

## Docker Postgres (psql) prompts
Run this to show all tables currently in the Postgres database
```
docker exec -it taskdb psql -U postgres -d tasks -c "\dt"
```
Run this to show the list of tasks in the Postgres database
```
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```
Run this to exit the psql CLI
```
docker exec -it taskdb psql -U postgres -d tasks -c "\q"
```

## API Endpoints

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Information | `200` |
| `GET` | `/health` | Health Check | `200` |
| `GET` | `/tasks` | List all tasks | `200` |
| `GET` | `/tasks/{id}` | Get task by ID | `200`, `404` |
| `POST` | `/tasks` | Create a new task | `201`, `400` |
| `PUT` | `/tasks/{id}` | Update title/done status | `200`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete a task | `204`, `404` |

---

## Verification Example (cURL)

```bash
curl -i http://localhost:8000/tasks
```

**Sample Output:**
```http
HTTP/1.1 200 OK
content-length: 196
content-type: application/json

[
  {"id":1,"title":"Buy boba tea","done":false},
  {"id":2,"title":"Go grocery shopping","done":false},
  {"id":3,"title":"Clean the house","done":true}
]
```

---

## Database Verification Screenshot / Output

Verified in container using `psql`:
```sql
tasks=# \dt
        List of relations
 Schema |  Name  | Type  | Owner 
--------+--------+-------+-------
 public | tasks  | table | postgres

tasks=# SELECT * FROM tasks;
 id |            title            | done 
----+-----------------------------+------
  1 | Buy boba tea                | f
  2 | Go grocery shopping         | f
  3 | Clean the house             | t
```

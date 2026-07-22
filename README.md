# BE-W3-A3-Containerize-your-stack
## W3 A3 Repo

## Docker container run command
Run the following command in your CLI
```
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
```
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


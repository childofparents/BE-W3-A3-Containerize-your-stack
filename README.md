# BE-W3-A3-Containerize-your-stack
## W3 A3 Repo

## Docker container run command
Run the following command in your CLI
```
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
```

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, col

# ---------------------------------------------------------------------------
# Stage 1: Load environment & create Postgres engine
# ---------------------------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. Check your .env file!")

# Create Postgres engine using SQLModel
engine = create_engine(DATABASE_URL, echo=False)


class Task(SQLModel, table=True):
    """The `tasks` table in Postgres."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False


def create_db_and_tables():
    """Create tasks table in Postgres if it doesn't exist."""
    SQLModel.metadata.create_all(engine)


def seed_tasks():
    """Insert the three example tasks, but only the very first time the table is empty."""
    with Session(engine) as session:
        first_row = session.exec(select(Task)).first()
        if first_row is None:
            session.add_all([
                Task(title="Buy boba tea", done=False),
                Task(title="Go grocery shopping", done=False),
                Task(title="Clean the house", done=True),
            ])
            session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_tasks()
    yield


app = FastAPI(lifespan=lifespan)


# ---------------------------------------------------------------------------
# Request/Response Models
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
async def root():
    """Describe this API and list its main endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoint": ["/tasks"]}


@app.get("/health")
async def health():
    """Check that the server is up and running."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Task Endpoints (Backed by Postgres)
# ---------------------------------------------------------------------------
@app.get("/tasks")
async def get_tasks(search: Optional[str] = None):
    """List all tasks live from Postgres, with optional title search."""
    with Session(engine) as session:
        statement = select(Task)

        if search and search.strip():
            statement = statement.where(col(Task.title).contains(search.strip()))

        tasks = session.exec(statement).all()
        return tasks


# ---------------------------------------------------------------------------
# Stage 2: Read endpoints backed by Postgres
# ---------------------------------------------------------------------------

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """Fetch a single task by ID from Postgres."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if task is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"}
            )

        return task

# ---------------------------------------------------------------------------
# Stage 3: Create, update, and delete endpoints backed by Postgres
# ---------------------------------------------------------------------------
@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task in Postgres with done set to false."""
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "title is required"})

    new_task = Task(title=task.title.strip(), done=False)
    with Session(engine) as session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, update: TaskUpdate):
    """Update a task's title and/or done status in Postgres."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if task is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Task {task_id} not found"}
            )

        if update.title is None and update.done is None:
            return JSONResponse(
                status_code=400,
                content={"error": "provide title and/or done to update"}
            )

        if update.title is not None and not update.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "title cannot be empty"}
            )

        if update.title is not None:
            task.title = update.title.strip()
        if update.done is not None:
            task.done = update.done

        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task from Postgres."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        task = session.exec(statement).first()

        if task is None:
            return JSONResponse(
                status_code=404,
                content={"error": f"Task {task_id} not found"}
            )

        session.delete(task)
        session.commit()
        return Response(status_code=204)
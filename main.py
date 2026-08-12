from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()}
    )
class TaskCreate(BaseModel):
    title: str = Field(min_length=3)
class TaskUpdate(BaseModel):
    title: str = Field(min_length=3)
    done: bool
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build my API",
        "done": False
    },
    {
        "id": 3,
        "title": "Learn Git",
        "done": True
    }
]

@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_update.title
            task["done"] = task_update.done
            return task

    raise HTTPException(status_code=404, detail="Task not found")
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task

    raise HTTPException(status_code=404, detail="Task not found")
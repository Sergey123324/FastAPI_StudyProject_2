from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy_orm.session import Session
from Models import User, Task, Base
from Database import get_session
from Schemas import UserCreate, TaskCreate, UserResponse, TaskResponse

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def new_user(user : UserCreate,session : Session = Depends(get_session)):
    new_user = User(
        username = user.username,
        email = user.email
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@app.post("/users/{user_id}/tasks", response_model=TaskResponse)
def user_tasks(user_id : int, task : TaskCreate, session : Session = Depends(get_session)):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )

    new_task = Task(
        title = task.title,
        description = task.description,
        user_id = user_id
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task

@app.get("/users/{user_id}/tasks", response_model=list[TaskResponse])
def get_tasks(user_id : int, session : Session = Depends(get_session)):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )
    tasks = session.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id : int, session : Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code = 404,
            detail = "Task not found!"
        )
    return task

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id : int, session : Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found!"
        )
    session.delete(task)
    session.commit()

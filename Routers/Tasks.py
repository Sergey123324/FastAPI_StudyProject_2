from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Database import get_session
from Models import Task, User
from Schemas import TaskCreate, TaskResponse
from Security.Auth import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    task = Task(
        title=data.title,
        description=data.description,
        user_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this task"
        )

    return task

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).all()

    return tasks

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this task"
        )

    task.title = data.title
    task.description = data.description

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this task"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted"
    }
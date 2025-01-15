from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user found')
    return task


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], createtask: CreateTask):
    user = db.scalar(select(User).where(User.id == createtask.user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user found')
    db.execute(insert(Task).values(title=createtask.title,
                                   content=createtask.content,
                                   priority=createtask.priority,
                                   completed=False,
                                   user_id=createtask.user_id,
                                   slug=slugify(createtask.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, updatetask: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user found')
    db.execute(update(Task).where(Task.id == task_id).values(
        title=updatetask.title,
        content=updatetask.content,
        priority=updatetask.priority,
        completed=updatetask.completed,
        user_id=updatetask.user_id,
        slug=slugify(updatetask.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful'}

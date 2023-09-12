from typing import List

from sqlalchemy import select, Delete
from sqlalchemy.orm import Session
from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:  # ToDo를 List에 담아서 반환한다
    return list(session.scalars(select(ToDo)))


def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))


def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()  # db save -> db에서 id를 할당! todo에는 id값이 존재 x
    session.refresh(instance=todo)  # id값이 todo에는 없기에 db에서 read하면 instance todo에 id값이 반영된다
    return todo


def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()  # db save -> db에서 id를 할당! todo에는 id값이 존재 x
    session.refresh(instance=todo)  # id값이 todo에는 없기에 db에서 read하면 instance todo에 id값이 반영된다
    return todo


def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(Delete(ToDo).where(ToDo.id == todo_id))
    session.commit()



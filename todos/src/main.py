from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema

from models.karlo import t2i

REST_API_KEY = '017c8acecb09c4f7ec5da1d79773218b'

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
):
    # ret = list(todo_data.values())
    todos: List[ToDo] = get_todos(session=session)

    if order and order == "DESC":
        return ToDoListSchema(
            shp=[ToDoSchema.model_validate(todo, from_attributes=True) for todo in todos[::-1]]
        )
    # return todos
    return ToDoListSchema(
        shp=[ToDoSchema.model_validate(todo, from_attributes=True) for todo in todos]
    )


# @app.get("/todos/{todo_id}", status_code=200)
# def get_todo_handler(
#         todo_id: int,
#         session: Session = Depends(get_db)
# ) -> List[ToDoSchema]:
#     # todo = todo_data.get(todo_id)
#     todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
#     if todo:
#         return [ToDoSchema.model_validate(todo, from_attributes=True)]
#     raise HTTPException(status_code=404, detail="Todo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateTodoRequest,  # RequestBody
        session: Session = Depends(get_db)
) -> List[ToDoSchema]:
    todo: ToDo = ToDo.create(request=request)  # pydantic -> orm, id=None
    todo: ToDo = create_todo(session=session, todo=todo)  # db에 todo값 post후, 다시 read하고 id값 반영해서 todo에 저장
    # todo_data[request.id] = request.model_dump()
    return [ToDoSchema.model_validate(todo, from_attributes=True)]


@app.post("/karlo/{prompt}", status_code=201)
def create_todo_handler(
        prompt: str,

        session: Session = Depends(get_db)
) -> List[ToDoSchema]:
    r = t2i(prompt, "", REST_API_KEY=REST_API_KEY)
    img_url = r.get("images")[0].get("image")
    todo: ToDo = ToDo.create_karlo(image_url=img_url)  # pydantic -> orm, id=None
    todo: ToDo = create_todo(session=session, todo=todo)  # db에 todo값 post후, 다시 read하고 id값 반영해서 todo에 저장
    # todo_data[request.id] = request.model_dump()
    return [ToDoSchema.model_validate(todo, from_attributes=True)]


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db)
) -> List[ToDoSchema]:
    # todo = todo_data.get(todo_id)
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return [ToDoSchema.model_validate(todo, from_attributes=True)]
    raise HTTPException(status_code=404, detail="Todo Not Found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    delete_todo(session=session, todo_id=todo_id)

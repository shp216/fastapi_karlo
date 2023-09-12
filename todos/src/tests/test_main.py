from database.orm import ToDo


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(client, mocker):
    response = client.get("/todos")
    assert response.status_code == 200

    # ASC
    mocker.patch("main.get_todos", return_value=[
        ToDo(id=1, contents="FASTAPI Section 0", is_done=True),
        ToDo(id=2, contents="FASTAPI Section 1", is_done=False),

    ])

    assert response.json() == {
        "shp": [
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
            {"id": 5, "contents": "string", "is_done": True},
            {"id": 6, "contents": "string", "is_done": False}
        ]
    }

    # DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "shp": [
            {"id": 6, "contents": "string", "is_done": False},
            {"id": 5, "contents": "string", "is_done": True},
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
        ]
    }


def test_get_todo(client, mocker):
    #200
    mocker.patch("main.get_todo_by_todo_id",
                 return_value=ToDo(id=29, contents="FASTAPI Section 1", is_done=False),
                 )
    response = client.get("/todos/29")
    assert response.status_code == 200
    assert response.json() == [{"id": 29, "contents": "FASTAPI Section 1", "is_done": False}]

    #404
    mocker.patch("main.get_todo_by_todo_id",
                 return_value=None
                 )
    response = client.get("/todos/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo Not Found"}

def test_create_todo(client, mocker):
    mocker.patch("main.create_todo",
                 return_value=None
                 )

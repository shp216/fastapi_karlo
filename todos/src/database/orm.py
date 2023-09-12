from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

from schema.request import CreateTodoRequest

Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"ToDO(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    @classmethod
    def create(cls, request: CreateTodoRequest) -> "ToDo":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )
        # id는 DB에서 결정해주기에 server에서 관리하지 않아도 된다.

    @classmethod
    def create_karlo(cls, image_url) -> "ToDo":
        return cls(
            contents=image_url,
            is_done=False
        )
        # id는 DB에서 결정해주기에 server에서 관리하지 않아도 된다.

    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self

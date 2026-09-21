from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(50))
    email : Mapped[str] = mapped_column(String(100))

    tasks : Mapped[list["Task"]] = relationship(back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(50))
    description : Mapped[str] = mapped_column(String(200))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    user : Mapped["User"] = relationship(back_populates="tasks")
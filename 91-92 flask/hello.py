from flask import Flask, render_template
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, ForeignKey, delete
from typing import List

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates='tasks')

    def __repr__(self):
        return f"{self.id} - {self.name}"

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user')

    def __repr__(self):
        return f"{self.telegram_id} - {self.name}"

class Produkt(Base):
    __tablename__ = 'produkt'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]


    def __repr__(self):
        return f"{self.name} - {self.price}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:\\Users\\1\\Documents\\Иванов Сергей\\Python\\DZ\\91-92 flask\\bot_tudu'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
todo = [{'id': 1, 'name': 'спать'}, {'id': 2, 'name': 'бежать'}, {'id': 3, 'name': 'пить'}]

@app.route('/')
def main():
    todo_db = db.session.execute(db.select(Task)).scalars().all()
    users = db.session.execute(db.select(User)).scalars().all()
    produkts = db.session.execute(db.select(Produkt)).scalars().all()
    return render_template('mail.html', todo_data=todo_db, users=users, produkts=produkts)

@app.route('/1')
def main2():
    return render_template('about.html')


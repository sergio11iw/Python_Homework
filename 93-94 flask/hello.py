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
    status: Mapped[str]

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.status}"

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user')

    def __repr__(self):
        return f"{self.telegram_id} - {self.name}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:\\Users\\1\\Documents\\Иванов Сергей\\Python\\DZ\\91-92 flask\\bot_tudu'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
todo = [{'id': 1, 'name': 'спать'},
        {'id': 2, 'name': 'бежать'},
        {'id': 3, 'name': 'пить'}]

@app.route('/')
def main():
    todo_db = db.session.execute(db.select(Task)).scalars().all()
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('mail.html', todo_data=todo_db, users=users)

@app.route('/about')
def main2():
    return render_template('about.html')

@app.route('/tasks/<int:user_id>')
def user_tasks(user_id):
    tasks = db.session.execute(db.select(Task).filter_by(user_id=user_id)).scalars().all()
    return render_template('tasks.html', tasks=tasks, user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)


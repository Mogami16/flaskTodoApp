from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass



db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db.init_app(app)

class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80))
    complete : Mapped[bool] = mapped_column()




@app.route("/")
def index():
    todos = db.session.execute(db.select(Todo)).scalars()
    return render_template("index.html", todos=todos.all())


@app.route("/add", methods= ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title= title, complete= False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/complete/<string:id>")
def complete(id):
    todo = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def delete(id):
    todo = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)


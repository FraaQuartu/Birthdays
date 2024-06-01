from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///birthdays.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

class Birthday(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    month: Mapped[int]
    day: Mapped[int]

with app.app_context():
    db.create_all()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Prendi l'input dal corpo della richiesta
        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day")) 

        # Inserisci l'elemento nel database
        if 1 <= month <= 12 and 1 <= day <= 31:
            birthday = Birthday(name=name, month=month, day=day)
            db.session.add(birthday)
            db.session.commit()

        return redirect("/")

    else:
        # Query dal db
        select = db.select(Birthday).order_by(Birthday.id.asc())
        birthdays_sqlalchemy = db.session.execute(select).scalars()

        return render_template("birthdays.html", birthdays=birthdays_sqlalchemy)


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")

    birthday = Birthday.query.filter_by(id=id).first()
    db.session.delete(birthday)
    db.session.commit()

    

    return redirect("/")

# Questa è chiamata sempre dalla home
@app.route("/modify", methods=["GET", "POST"])
def modify():
    if request.method == "GET":
        id = request.args.get("id")
        return render_template("modify.html", id=id)

    else:
        id = request.form.get("id")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        # Query per modificare
        birthday = Birthday.query.filter_by(id=id).first()
        birthday.month = month
        birthday.day = day
        db.session.commit()        

        return redirect("/")
    

@app.context_processor
def utility_processor():
    def format_date(month, day):
        return f"{month}/{day}"
    return dict(format_date=format_date)
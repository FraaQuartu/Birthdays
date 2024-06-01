import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session





app = Flask(__name__)

db = SQL("sqlite:///birthdays.db")

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
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:
        # Query dal db
        birthdays = db.execute("SELECT * FROM birthdays")
        

        # Formatta le date
        for b in birthdays:
            b["date"] = f"{b["month"]}/{b["day"]}"

        print(birthdays)
        return render_template("birthdays.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")

    db.execute("DELETE FROM birthdays WHERE id = ?", id);

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
        db.execute("UPDATE birthdays SET month = ?, day = ? WHERE id = ?", month, day, id)

        return redirect("/")
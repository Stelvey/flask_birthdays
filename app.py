import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = sqlite3.connect("birthdays.db", check_same_thread=False)


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

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        id = request.form.get("id")

        if id:
            db.execute("DELETE FROM birthdays WHERE id = ?", (id,))
        elif db.execute("SELECT name FROM birthdays WHERE name = ?", (name,)).fetchall():
            db.execute("UPDATE birthdays SET month = ?, day = ? WHERE name = ?", (month, day, name))
        elif name and month and day:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, month, day))

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        entries = db.execute("SELECT * FROM birthdays").fetchall()

        return render_template("index.html", entries=entries)



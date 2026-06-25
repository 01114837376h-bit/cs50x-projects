import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy import false

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
print("Current directory:", os.getcwd())
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = SQL(f"sqlite:///{os.path.join(BASE_DIR, 'birthdays.db')}")


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
        if not name or not month or not day:
            flash("Please fill in all fields.")
            return redirect("/")
        check_existing = db.execute("SELECT * FROM birthdays WHERE name = ? AND month = ? AND day = ?", name, month, day)
        if len(check_existing)>0:
            flash("Birthday already exists.")
            return redirect("/")
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        flash("Birthday added successfully.")
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=false)
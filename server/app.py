import sqlite3

from flask import Flask, render_template, g, request


app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

# tells flask , if we ever need to use the database , here is where the database files lives.
app.config["DATABASE"] = "database/fitfusion.db"


def get_db_connection():
    """OPEN a connection to a sqlite database. we attach it to 'g' so 
    it can be reused within a single request"""

    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row  # so i can access columns by name
        g.db = conn
    return g.db


# Run the decorated function after every request, no matter what happens
@app.teardown_appcontext
def close_db_connection(exception=None):
    """Automatically close the DB connection at the end of each request"""

    # Try to take "db" out of the backpack(g), If it exists → give me the connection object, If it doesn’t → give me None , We are cleaning the backpack.
    db = g.pop("db", None)
    # Did we actually have a database connection in this request? if db is none , do nothing.
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/back-squat.html", methods=["GET", "POST"])
def back_squat():

    # 1) open Database(db) connection
    db = get_db_connection()

    # 2) look up the exercise row for ' back_squat '
    exercise = db.execute(
        # fetchone return a row like {"id":1} if found or None if no such exercise exist.
        "SELECT id FROM exercises WHERE slug = ?", ("back_squat",)).fetchone()

    if exercise is None:
        # this means the exercise table doesn't have 'back_squat'
        print("ERROR: 'back_squat' not found in exercises table!")
        return "exercise not found", 404

    exercise_id = exercise["id"]
    # this is TEMPORARY!!
    user_id = 1

    # 3) handles form submission (POST)
    if request.method == "POST":
        # for this step we just read the form values.
        weight = request.form.get("weight")
        # set is a build in python function so to not confuse the 2 i use sets_ .
        sets_ = request.form.get("sets")
        reps = request.form.get("reps")

        # insert the new log row into workout_logs with this user, this exercise, this weight , these reps, and these sets.
        db.execute(
            """INSERT INTO workout_logs (user_id, exercise_id, weight, sets, reps) VALUES(?,?,?,?,?)""",
            (user_id, exercise_id, weight, sets_, reps)
        )
        # this makes the changes permanent , without this the insert would be temporary.
        db.commit()

        print("LOG SAVED:",
              "user_id=", user_id,
              "exercise_id=", exercise_id,
              "weight=", weight,
              "reps=", reps,
              "sets=", sets_
              )

    # always load logs (for both GET and after POST)
    logs = db.execute(
        """
        SELECT weight, sets, reps, logged_at FROM workout_logs
        WHERE user_id = ? AND exercise_id = ?
        ORDER BY logged_at DESC
        """,
        (user_id, exercise_id)
    ).fetchall()

    return render_template("back-squat.html", logs=logs)


@app.route("/chest.html")
def chest():
    return render_template("chest.html")


@app.route("/back.html")
def back():
    return render_template("back.html")


@app.route("/arms.html")
def arms():
    return render_template("arms.html")


@app.route("/shoulders.html")
def shoulders():
    return render_template("shoulders.html")


@app.route("/triceps.html")
def triceps():
    return render_template("triceps.html")


@app.route("/debug/exercises")
def debug_exercises():
    db = get_db_connection()
    rows = db.execute(
        "SELECT slug, name, muscle_group FROM exercises").fetchall()
    return "<br>".join(f"{row['slug']} - {row['name']} ({row['muscle_group']})" for row in rows)


if __name__ == "__main__":
    app.run(debug=True)

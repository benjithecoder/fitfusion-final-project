import sqlite3
from flask import Flask, render_template, g, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

# flask stores the session in a cookie in the browser, without it session["user_id"] won't work
app.secret_key = "dev-secret-change-this-later"


# tells flask , if we ever need to use the database , here is where the database files lives.
app.config["DATABASE"] = "database/fitfusion.db"


def get_db_connection():
    """OPEN a connection to a sqlite database. we attach it to 'g' so 
    it can be reused within a single request"""

    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"])
        # so i can access columns by name not with indexes.
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


# Run the decorated function after every request, no matter what happens and if a connection has been opened close it.
@app.teardown_appcontext
def close_db_connection(exception=None):
    """Automatically close the DB connection at the end of each request"""

    # Try to take "db" out of the backpack(g), If it exists → give me the connection object, If it doesn’t → give me None , We are cleaning the backpack.
    db = g.pop("db", None)
    # Did we actually have a database connection in this request? if db is none , do nothing.
    if db is not None:
        db.close()


@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db_connection()

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password_hash = request.form.get("password_hash", "")

        # basic validation , no empty values
        if not email or not password_hash:
            return "email and password are required", 400

        # hash the password so we never store plain text
        hashed_password = generate_password_hash(password_hash)

        try:
            # try to insert the new user
            db.execute(
                "INSERT INTO users (email, password_hash) VALUES (?,?)",
                (email, hashed_password)
            )
            db.commit()
        except sqlite3.IntegrityError:
            # this happens when username is already used (because of UNIQUE)
            return "email already taken", 400

        # get the new user's id
        user = db.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)  # you need to add ' , 'to make sure it is not a string otherwise you would send email as a string and not as a 1-item tuple
            # fetchone is only used when you expect 1 result not 2 , not 100 , i only need 1 id so that's why fetchONE
        ).fetchone()

        # log the user in immediately after registering
        session["user_id"] = user["id"]

        return "Registered! ('ll add proper redirect + login page next)"

    # GEt request --> just show the registration form
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db_connection()

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password_hash = request.form.get("password_hash", "")

        # 1) look up user by username
        user = db.execute(
            "SELECT id , password_hash FROM users WHERE email = ?",
            (email,)  # you need to add ' , 'to make sure it is not a string otherwise you would send email as a string and not as a 1-item tuple
        ).fetchone()

        if user is None:
            return "Invalid email", 400

        # 2) check the password against the stored hash
        stored_hash = user["password_hash"]

        if not check_password_hash(stored_hash, password_hash):
            return "Invalid password", 400

        # 3) if we get here, login is successful -> remember the user in the session
        session["user_id"] = user["id"]

        return redirect(url_for("home"))

    # GET request -> show the login form
    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove everything the session (including user_id)
    session.clear()

    # send the user to the login page
    return redirect(url_for("login"))


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

    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("login"))

    edit_log_id = None

    # 3) handles form submission (POST)
    if request.method == "POST":
        # did this POST come from the delete button?
        delete_id = request.form.get("delete_log_id")
        update_id = request.form.get("update_log_id")
        edit_id = request.form.get("edit_log_id")

        if delete_id:
            # Delete the specific log row that matches this id
            db.execute(
                """DELETE FROM workout_logs
                WHERE id = ? AND user_id = ? AND exercise_id = ?""",
                (delete_id, user_id, exercise_id)
            )
            db.commit()

        elif update_id:
            # save changes for existing log (UPDATE)
            weight = request.form.get("weight")
            sets_ = request.form.get("sets")
            reps = request.form.get("reps")

            db.execute(
                """UPDATE workout_logs 
                SET weight = ?, sets = ?, reps = ?
                WHERE id = ? AND user_id = ? AND exercise_id = ?""",
                (weight, sets_, reps, update_id, user_id, exercise_id)
            )
            db.commit()

        elif edit_id:
            # put this row into edit mode no DB changes yet
            edit_log_id = int(edit_id)

        else:
            # otherwise, it's a normal "save log" submission
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

    # always load logs (for both GET and after POST)
    logs = db.execute(
        """
        SELECT id, weight, sets, reps, logged_at FROM workout_logs
        WHERE user_id = ? AND exercise_id = ?
        ORDER BY logged_at DESC
        """,
        (user_id, exercise_id)
    ).fetchall()

    return render_template("back-squat.html", logs=logs, edit_log_id=edit_log_id)


@app.route("/chest.html", methods=["GET", "POST"])
def chest():
    # 1) open Database(db) connection
    db = get_db_connection()

    # 2) look up the exercise row for ' bench_press'
    exercise = db.execute(
        # fetchone return a row like {"id":1} if found or None if no such exercise exist.
        "SELECT id FROM exercises WHERE slug = ?", ("bench_press",)).fetchone()

    if exercise is None:
        # this means the exercise table doesn't have 'bench_press'
        print("ERROR: 'bench_press' not found in exercises table!")
        return "exercise not found", 404

    exercise_id = exercise["id"]

    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("login"))

    edit_log_id = None

    # 3) handles form submission (POST)
    if request.method == "POST":
        # did this POST come from the delete button?
        delete_id = request.form.get("delete_log_id")
        update_id = request.form.get("update_log_id")
        edit_id = request.form.get("edit_log_id")

        if delete_id:
            # Delete the specific log row that matches this id
            db.execute(
                """DELETE FROM workout_logs
                WHERE id = ? AND user_id = ? AND exercise_id = ?""",
                (delete_id, user_id, exercise_id)
            )
            db.commit()

        elif update_id:
            # save changes for existing log (UPDATE)
            weight = request.form.get("weight")
            sets_ = request.form.get("sets")
            reps = request.form.get("reps")

            db.execute(
                """UPDATE workout_logs 
                SET weight = ?, sets = ?, reps = ?
                WHERE id = ? AND user_id = ? AND exercise_id = ?""",
                (weight, sets_, reps, update_id, user_id, exercise_id)
            )
            db.commit()

        elif edit_id:
            # put this row into edit mode no DB changes yet
            edit_log_id = int(edit_id)

        else:
            # otherwise, it's a normal "save log" submission
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

    # always load logs (for both GET and after POST)
    logs = db.execute(
        """
        SELECT id, weight, sets, reps, logged_at FROM workout_logs
        WHERE user_id = ? AND exercise_id = ?
        ORDER BY logged_at DESC
        """,
        (user_id, exercise_id)
    ).fetchall()

    return render_template("chest.html", logs=logs, edit_log_id=edit_log_id)


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


@app.route("/debug-session")
def debug_session():
    print("SESSION CONTENTS:", dict(session))
    return {"session": dict(session)}


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask

# create the main app object
app = Flask(
    __name__,
    static_folder="")


# say's "when someone visits / , run the home() function"
@app.route("/")
def home():
    """
    Very first test route. for now it just return simple text so i can confirm the server works.
    """
    return "Fitfusion backend is running 🚀"


# let's you start a local server with python app.py
if __name__ == "__main__":
    # debug=True auto-reloads the server when you change python files.
    app.run(debug=True)

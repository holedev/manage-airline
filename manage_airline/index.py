from flask import render_template
from manage_airline import app


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)

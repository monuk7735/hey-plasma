from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route("/")
def home():
    users = []
    user = {
        "name": "Rohan Verma",
        "address": "South Delhi, New Delhi",
        "pin": "400001",
        "blood": "A+"
    }
    users = [user]*10
    return render_template('home.html', users=users)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        return "doing registration"

    return "register"


@app.route("/login")
def login():
    return "login"


@app.route("/requests")
def connected_users():
    return "connected users"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run("0.0.0.0", 7735)

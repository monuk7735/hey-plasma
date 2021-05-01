from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    users = []
    user = {
        "name" : "Rohan Verma",
        "address" : "South Delhi, New Delhi",
        "pin" : "400001",
        "blood" : "A+"
    }
    users = [user]*10
    print(users)
    return render_template('home.html', users=users)


@app.route("/register")
def register():
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

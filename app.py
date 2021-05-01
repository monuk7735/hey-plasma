from flask import Flask, request, render_template, redirect
from pprint import pprint

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
        name = request.form['name']
        blood_group = request.form['blood']
        address_city = request.form['address-city']
        address_state = request.form['address-state']
        address_pin = request.form['address-pin']
        email = request.form['email']
        password = request.form['password']
        # TODO Do registration
        return "doing registration"

    return redirect("/login")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # TODO Do Login
        return "doing login"
    return render_template("login.html")


@app.route("/requests")
def connected_users():
    return "connected users"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run("0.0.0.0", 7735)

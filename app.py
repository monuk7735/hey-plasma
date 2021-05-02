import json

from flask import Flask, request, render_template, redirect
from supabase_py import Client, create_client

import local.secret as secret

app = Flask(__name__)

url:str = secret.SUPABASE_URL
key:str = secret.SUPABASE_KEY
supabase:Client = create_client(url, key)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/users")
def get_users():
    users = []
    user = {
        "name": "Rohan Verma",
        "address": "South Delhi, New Delhi",
        "pin": "400001",
        "blood": "O+",
        "uid" : "8743br384"
    }
    users = [user]*10
    return json.dumps(users)

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

        user = supabase.auth.sign_up(email=email, password=password)
        if 'error' in user:
            return user['error_description']
            # {'id': 'cf53f40e-2649-4c41-89c4-3aca64f3d936', 'aud': 'authenticated', 'role': 'authenticated', 'email': 'admin@admin.admin', 'confirmation_sent_at': '2021-05-02T07:53:00.0062947Z', 'app_metadata': {'provider': 'email'}, 'user_metadata': None, 'created_at': '2021-05-02T07:53:00.004806Z', 'updated_at': '2021-05-02T07:53:00.635398Z', 'status_code': 200}
        uid = user['id']

        # TODO Do registration

        return "doing registration"

    return redirect("/login")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = supabase.auth.sign_in(email=email, password=password)

        if 'error' in user:
            return user['error_description']

        return "login success"
    return render_template("login.html")


@app.route("/requests")
def connected_users():
    return "connected users"

@app.route("/request")
def connected_to_user():
    uid = request.form['uid']
    return "connected users"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run("0.0.0.0", 7735)

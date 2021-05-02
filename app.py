import os
import json

from flask import Flask, request, render_template, redirect, send_from_directory
from supabase_py import Client, create_client

app = Flask(__name__)

url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'assets/favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def home():
    if supabase.auth.current_user:
        authenticated = True
    else:
        authenticated = False
    return render_template('home.html', authenticated=authenticated)


@app.route("/api/users")
def get_users():
    users = []
    user = {
        "name": "Rohan Verma",
        "city": "South Delhi",
        "state": " New Delhi",
        "pin": "400001",
        "blood": "O+",
        "uid": "8743br384-36vb443-q36dsfs"
    }
    users = [user]*10
    return json.dumps(users)


@app.route("/register", methods=['POST'])
def register():
    name = request.form['name']
    blood_group = request.form['blood']
    address_city = request.form['address-city']
    address_state = request.form['address-state']
    address_pin = request.form['address-pin']
    email = request.form['email']
    password = request.form['password']

    result = supabase.auth.sign_up(email=email, password=password)

    print(result)

    if result['status_code'] != 200:
        return result
        # {'id': 'cf53f40e-2649-4c41-89c4-3aca64f3d936', 'aud': 'authenticated', 'role': 'authenticated', 'email': 'admin@admin.admin', 'confirmation_sent_at': '2021-05-02T07:53:00.0062947Z', 'app_metadata': {'provider': 'email'}, 'user_metadata': None, 'created_at': '2021-05-02T07:53:00.004806Z', 'updated_at': '2021-05-02T07:53:00.635398Z', 'status_code': 200}

    try:
        uid = result['user']['id']
    except:
        print("error")

    # TODO Do registration

    return "doing registration"


@app.route("/login", methods=['POST', 'GET'])
def login():
    if supabase.auth.current_user:
        return redirect("/")
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = supabase.auth.sign_in(email=email, password=password)

        if 'error' in user:
            return user['error_description']

        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    supabase.auth.sign_out()
    return redirect('/')


@app.route("/requests")
def connected_users():
    return "connected users"


@app.route("/request", methods=['POST'])
def connected_to_user():
    if not supabase.auth.current_user:
        return {
            "status": 0,
            "message": "Not Logged IN"
        }
    uid = request.form['uid']
    return {
        "status": 1,
        "message": "Request Made to " + uid
    }


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run("0.0.0.0", 7735)

import os
import json

from flask import Flask, request, render_template, redirect, send_from_directory
from supabase_py import Client, create_client
from pytezos import pytezos

app = Flask(__name__)

pyt = pytezos.using(key=os.environ["TEZOS_KEY"],
                    shell="https://edonet.smartpy.io")
contr = pyt.contract(os.environ["CONTRACT_ADDRESS"])


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
    allData = contr.storage()
    users = []
    exludeid=""
    if supabase.auth.current_user:
        exludeid=supabase.auth.current_user['id']
    for item in allData:
        userdata = allData[item]
        if item != exludeid:
            users.append({
                "name": userdata["name"],
                "address": userdata["address"],
                "pin": userdata["pincode"],
                "blood": userdata["bloodGroup"],
                "canDonate": userdata["canDonate"],
                "uid": item
            })
    return json.dumps(users)


@app.route("/register", methods=['POST','GET'])
def register():
    if request.method == "GET":
        return redirect('/login')
    name = request.form['name']
    blood_group = request.form['blood']
    address_city = request.form['address-city']
    address_state = request.form['address-state']
    address_pin = request.form['address-pin']
    email = request.form['email']
    password = request.form['password']
    phone=request.form['phone']

    result = supabase.auth.sign_up(email=email, password=password)

    print(result)

    if result['status_code'] != 200:
        return result
        # {'id': 'cf53f40e-2649-4c41-89c4-3aca64f3d936', 'aud': 'authenticated', 'role': 'authenticated', 'email': 'admin@admin.admin', 'confirmation_sent_at': '2021-05-02T07:53:00.0062947Z', 'app_metadata': {'provider': 'email'}, 'user_metadata': None, 'created_at': '2021-05-02T07:53:00.004806Z', 'updated_at': '2021-05-02T07:53:00.635398Z', 'status_code': 200}

    supabase.auth.sign_in(email=email, password=password)

    try:
        uid = result['user']['id']
    except:
        print("error")

    contr.createUser(uid=uid,
        username=name,
        phone=phone,
        address= address_city+", "+address_state,
        canDonate=True,
        email=email,
        bloodGroup=blood_group,
        pincode=address_pin).inject()

    return redirect("/")


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


@app.route("/profile")
def connected_users():
    if supabase.auth.current_user:
        uid=supabase.auth.current_user['id']
        data = contr.storage()[uid]
        return render_template("connected_users.html",user=data,authenticated=True)
    else:
        return redirect('/login')
    


@app.route("/request", methods=['POST'])
def connected_to_user():
    if not supabase.auth.current_user:
        return {
            "status": 0,
            "message": "Not Logged IN"
        }
    uid = request.form['uid']
    curuid=supabase.auth.current_user['id']
    data = contr.storage()[curuid]
    contr.addRequest(
            requestedTo=uid,
            name=data["name"],
            phoneNumber=data["phone"],
            email=data["email"]
        ).inject()
    return {
        "status": 1,
        "message": "Request Made to " + uid
    }

@app.route("/changestatus", methods=['POST'])
def changeStatus():
    if not supabase.auth.current_user:
        return {
            "status": 0,
            "message": "Not Logged IN"
        }
    curuid=supabase.auth.current_user['id']
    canDonate = request.form['canDonate']
    t=True
    if canDonate == 'false':
        t=False
    contr.updateStatus(uid=curuid,canDonate=t).inject()
    return {
        "status": 1,
        "message": "Can Donate status updated"
    }

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", 7735)

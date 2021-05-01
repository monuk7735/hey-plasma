from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

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
    app.run("0.0.0.0",7735)
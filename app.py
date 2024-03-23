from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def practice():
    return render_template("practice.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/registration')
def registration():
    return render_template("registration.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")


# localhost:5000/user/ilya
@app.route('/user/<name>')
def user(name):
    return f"Hello {name}!"

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = "placeholder"

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.db'
# Initialize the Database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create __str__
    def __repr__(self):
        return f'{self.name}'
# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
    first_name = "Ilya"
    stuff = "This is bold text"

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)


# localhost:5000/user/ilya
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)


# Create Custom Error Pages

# Invalid URl
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Create Name Page
@app.route('/name', methods=["GET", "POST"])
def name():
    name = None
    form = NameForm()
    # Validate FOrm
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html", name=name, form=form)

from dotenv import load_dotenv
import os
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# load dotenv
load_dotenv()

# Create a Flask Instance
app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = "placeholder"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv("DB_KEY")
app.config['MYSQL_DB'] = 'flask_database'

mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{os.getenv('DB_KEY')}@localhost/flask_database"
# Initialize the Database
db = SQLAlchemy(app)


# sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create __str__
    def __repr__(self):
        return f'{self.name}'


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Update DataBase Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error, there was a problem... try again")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


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

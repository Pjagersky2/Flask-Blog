"""Module for learning Flask via Corey Schafer's tutorial"""
from datetime import datetime

from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# flask object where name = module name
app = Flask(__name__)

app.config["SECRET_KEY"] = "f1a9f9f191632a81c7cf5ee4b6096945"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User({self.username!r}, {self.email!r}, {self.image_file!r})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post({self.title!r}, {self.date_posted})"


posts = [
    {
        "author": "peter jagersky",
        "title": "blog post 1",
        "content": "first post content",
        "date_posted": "february 02, 2023"
    },
    {
        "author": "jane doe",
        "title": "blog post 2",
        "content": "second post content",
        "date_posted": "february 03, 2023"
    }
]


@app.route("/")
@app.route("/home")  # both paths take you to the same place
def home() -> str:
    """
    Handle the home page.

    This function handles the home page and returns the rendered
    template for the home page.

    Returns:
        str: A rendered template for the home page.
    """

    return render_template("home.html", posts=posts)


@app.route("/about")
def about() -> str:
    """
    Handle the about page.

    This function handles the about page and returns the rendered
    template for the about page.

    Returns:
        str: A rendered template for the about page.
    """

    return render_template("about.html", title="about")


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    Handle user registration.

    This function handles user registration and returns a rendered
    template for the registration page.

    Returns:
        str: A rendered template for the registration page.
    """

    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Handle user login authentication.

    This function handles user login and returns a rendered
    template for the login page.

    Returns:
        str: A rendered template for the login page.
    """

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("you have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("login unsuccessful.  please check username and password", "danger")

    return render_template("login.html", title="login", form=form)


if __name__ == "__main__":
    app.run(debug=True)

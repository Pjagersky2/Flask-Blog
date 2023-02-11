from flask import flash, redirect, render_template, url_for
from flaskblog import app
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import Post, User


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

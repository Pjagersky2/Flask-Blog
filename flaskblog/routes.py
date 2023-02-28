import os
import secrets
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flaskblog.models import Post, User

with app.app_context():
    db.create_all()

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
def home() -> render_template:
    """
    Handle the home page.

    This function handles the home page and returns the rendered
    template for the home page.

    Returns:
        function: A rendered template for the home page.
    """

    return render_template("home.html", posts=posts)


@app.route("/about")
def about() -> render_template:
    """
    Handle the about page.

    This function handles the about page and returns the rendered
    template for the about page.

    Returns:
        function: A rendered template for the about page.
    """

    return render_template("about.html", title="about")


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    Handle user registration.

    This function handles user registration and returns a rendered
    template for the registration page.

    Returns:
        str: A url redirect for the login page.
        function: A rendered template for the registration page.
    """

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash("Your account has been created, you may now log in.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Handle user login authentication.

    This function handles user login and returns a rendered
    template for the login page.

    Returns:
        str: A url redirect template for the home page.
        str: A rendered template for the login page.
    """

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")

            return redirect(next_page) if next_page else redirect(url_for("home"))

        else:
            flash("login unsuccessful.  please check email and password", "danger")

    return render_template("login.html", title="login", form=form)


@app.route("/logout")
def logout() -> str:
    """
    Handle user logout.

    This function handles user logout and redirects them to the home page.

    Returns:
        function: A url redirect for the home page.
    """

    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture) -> str:
    """
    Save the user's uploaded picture.

    This function will save a picture that a user has uploaded and change
    the name.

    Args:
        form_picture (str): the picture uploaded by the user.

    Returns:
        str: the filename of the user's uploaded picture.
    """

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics",
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account() -> str:
    """
    Handle user account.

    This function handles user accounts.

    Returns:
        function: A render template for the account page.
    """

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)

    return render_template("account.html", title="Account", image_file=image_file, form=form)

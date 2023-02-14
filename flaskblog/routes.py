from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm
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
        str: A redirect  for the login page.
        str: A rendered template for the registration page.
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
        str: A redirect template for the home page.
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
        str: A redirect for the home page.
    """

    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account() -> str:
    """
    Handle user account,

    This function handles user accounts and .

    Returns:
        str: A redirect for the home page.
    """

    return render_template("account.html", title="account")

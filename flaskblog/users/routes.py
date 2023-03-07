from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm,
                                   LoginForm,
                                   UpdateAccountForm,
                                   RequestResetForm,
                                   ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created, you may now log in.", "success")

        return redirect(url_for("users.login"))

    return render_template("register.html", title="register", form=form)


@users.route("/login", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")

            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        else:
            flash("login unsuccessful.  please check email and password", "danger")

    return render_template("login.html", title="login", form=form)


@users.route("/logout")
def logout() -> str:
    """
    Handle user logout.

    This function handles user logout and redirects them to the home page.

    Returns:
        function: A url redirect for the home page.
    """

    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)

    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")  # both paths take you to the same
# place
def user_posts(username) -> render_template:
    """
    Individual user posts.

    Show all posts from an individual user.

    Returns:
        function: A rendered template for a user's page.
    """

    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request() -> str:
    """
    Allows a user to request a password reset.

    The first part in allowing a user to request a password reset.
    """

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions how to reset your "
              "password.", "info")
        return redirect(url_for("users.login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token) -> str:
    """
    The user's reset token.

    The second part in allowing a user to request a password reset.
    """

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user.password = hashed_password
        db.session.commit()
        flash("Your password has been reset successfully.", "success")

        return redirect(url_for("users.login"))

    return render_template("reset_token.html",
                           title="Reset Password",
                           form=form)

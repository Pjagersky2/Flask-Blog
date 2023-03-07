from flask import Blueprint, render_template, request

from flaskblog.models import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")  # both paths take you to the same place
def home() -> render_template:
    """
    Handle the home page.

    This function handles the home page and returns the rendered
    template for the home page.

    Returns:
        function: A rendered template for the home page.
    """

    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)

    return render_template("home.html", posts=posts)


@main.route("/about")
def about() -> render_template:
    """
    Handle the about page.

    This function handles the about page and returns the rendered
    template for the about page.

    Returns:
        function: A rendered template for the about page.
    """

    return render_template("about.html", title="about")

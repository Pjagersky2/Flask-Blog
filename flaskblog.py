"""Module for learning Flask via Corey Schafer's tutorial"""
from flask import Flask, render_template, url_for

# flask object where name = module name
app = Flask(__name__)

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
def home():
    """The home directory of the flask webapp"""

    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    """The about directory of the flask webapp"""

    return render_template("about.html", title="about")


if __name__ == '__main__':
    app.run(debug=True)

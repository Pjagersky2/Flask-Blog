from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer

from flaskblog import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        Create password reset token.

        Creates a password reset token.
        """

        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")


    def __repr__(self):
        """
        Represents the User as a string.

        When the user object is printed it states username, email, and
        image file.

        Returns:
            str: The user's username, email, and image file.
        """

        return f"User({self.username!r}, {self.email!r}, {self.image_file!r})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """
        Represents the Post as a string.

        When the user object is printed it states title and date posted.

        Returns:
            str: The post's title and date posted.
        """

        return f"Post({self.title!r}, {self.date_posted})"

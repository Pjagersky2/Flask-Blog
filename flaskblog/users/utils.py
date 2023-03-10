import os
import secrets
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from flaskblog import mail


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
    picture_path = os.path.join(current_app.root_path, "static/profile_pics",
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user, base_url="http://localhost:5000"):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@test.com",
                  recipients=[user.email])
    msg.body = f"""
    To reset your password, please visit the following link: 
{base_url}{url_for("users.reset_token", token=token, external=True)}

If you did not make this request then ignore this email and no changes will 
be made.
    """

    mail.send(msg)

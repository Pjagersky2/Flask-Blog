from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# flask object where name = module name
app = Flask(__name__)

app.config["SECRET_KEY"] = "f1a9f9f191632a81c7cf5ee4b6096945"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# CS Flask video five 15:41
from flaskblog import routes

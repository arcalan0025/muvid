# Initialize SQL-Alchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

SQLDB = SQLAlchemy()
BCRYPT = Bcrypt()
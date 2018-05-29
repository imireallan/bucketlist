"""Module for our Models"""
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """Class that represents our users table"""

    # Ensures the table is in plural
    __tablename__ = "users"

    # defines the columns of the users tables
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    bucketlists = db.relationship(
        "Bucketlist", order_by="Bucketlist.id",
        cascade="all, delete-orphan"
    )

    def __init__(self, email, password):
        """Initialize the user with an email and a password"""
        self.email = email
        self.password = password

    @property
    def password(self):
        """Prevent the password from being accessed"""
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password):
        """Set Password Hash"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """check if hashed password matches actual password"""
        return check_password_hash(self.password_hash, password)



class Bucketlist(db.Model):
    """Class that represents our bucketlist table"""

    # ensures the table name is in plural
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """Initialize the bucketlist with a name and the owner"""
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


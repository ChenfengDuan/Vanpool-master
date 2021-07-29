from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

ACCESS = {
    'rider': 0,
    'driver': 1,
    'admin': 2
}


class User(UserMixin, db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=True,
        unique=True
    )
    email = db.Column(
        db.String(120),
        index=True,
        unique=True
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )

    access = db.Column(
        db.Integer,
        unique=False
    )
    vehicle = db.relationship('Vehicle', backref='driver', lazy='dynamic')

    def __init__(self, username=None, email=None, password=None, access=ACCESS['rider']):
        self.username = username
        self.email = email
        self.password = password
        self.access = access

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_rider(self):
        return self.access == ACCESS['rider']

    def is_driver(self):
        return self.access == ACCESS['driver']

    def is_admin(self):
        return self.access == ACCESS['admin']

    def print_users(self):
        users = User.query.all()
        string = ""
        for u in users:
            string = string + u.username + " "
        return string

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Vehicle(db.Model):

    __tablename__ = "vehicle"
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    color = db.Column(db.String(64))
    license_plate = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Vehicle: \nMake: {},\nModel: {},\nColor: {}>'.format(self.make, self.model, self.color)

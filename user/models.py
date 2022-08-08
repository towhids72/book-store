import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    api_key = db.Column(db.String(255), nullable=True, unique=True)
    is_admin = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<user {self.id} - {self.username}>'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'api_key': self.api_key,
            'is_admin': self.is_admin,
            'is_active': self.is_active
        }

    def update_api_key(self):
        if self.api_key is None:
            self.api_key = str(uuid.uuid4())

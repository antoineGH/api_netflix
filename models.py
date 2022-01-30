import datetime
from __init__ import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Account(db.Model):
    account_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "- ACCOUNT - account_id: {}, email: {}, first_name: {}, last_name: {}, date_created: {}".format(self.account_id, self.email, self.first_name, self.last_name, self.date_created)

    @property
    def serialize(self):
        return {
            'account_id': self.account_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_created
        }

class User(db.Model):
    user_id = Column(Integer, primary_key=True)
    profile = Column(String(200), nullable=False)
    account_id = Column(Integer, ForeignKey(Account.account_id), nullable=False)

    def __repr__(self):
        return "- USER - user_id: {}, profile: {}, account_id: {}".format(self.user_id, self.profile, self.account_id)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'profile': self.profile,
            'account_id': self.account_id,
        }

class List(db.Model):
    list_id = Column(Integer, primary_key=True)
    list_title = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)

    def __repr__(self):
        return "- LIST - list_id: {}, list_title: {}, user_id: {}".format(self.list_id, self.list_title, self.user_id)

    @property
    def serialize(self):
        return {
            'list_id': self.list_id,
            'list_title': self.list_title,
            'user_id': self.user_id,
        }

class Media(db.Model):
    media_id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, nullable=False)
    media_type = Column(String(200), nullable=False)
    list_id = Column(Integer, ForeignKey(List.list_id), nullable=False)

    def __repr__(self):
        return "MEDIA - media_id: {}, tmdb_id: {}, list_id: {}".format(self.media_id, self.tmdb_id, self.list_id)

    @property
    def serialize(self):
        return {
            'media_id': self.media_id,
            'tmdb_id': self.tmdb_id,
            'list_id': self.list_id,
        }


from sqlalchemy import Column, String
from sqlalchemy import Integer
from wtforms import Form, TextAreaField, validators

from modules import Base


class KeyValue(Base):
    __tablename__ = 'data'

    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def serializable(self):
        return


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(64))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '{} {} {}'.format(self.get_id(), self.username, self.email)



from wtforms import Form, TextAreaField, validators


class UserForm(Form):
    username = TextAreaField('Username:', validators=[validators.required()])
    email = TextAreaField('Email:', validators=[validators.required(), validators.length(min=6, max=35)])
    password = TextAreaField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
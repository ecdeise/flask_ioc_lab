from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    """Configure the application."""

    def configure(self, binder):
        # We configure the DB here, explicitly, as Flask-SQLAlchemy requires
        # the DB to be configured before request handlers are called.
        db = self.configure_db(self.app)
        binder.bind(SQLAlchemy, to=db, scope=singleton)
        binder.bind(Cache, to=Cache(self.app), scope=singleton)

    def configure_db(self, app):
        db = SQLAlchemy(app)
        Base.metadata.create_all(db.engine)
        # db.session.add_all([
        #     KeyValue('hello', 'world'),
        #     KeyValue('goodbye', 'cruel world'),
        # ])
        db.session.commit()
        return db

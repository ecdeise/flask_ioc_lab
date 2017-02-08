# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_cache import Cache
from flask_injector import FlaskInjector
from injector import Injector
from sqlalchemy.ext.declarative import declarative_base

import modules
import views

il = logging.getLogger('injector')
il.addHandler(logging.StreamHandler())
il.level = logging.DEBUG


# We use standard SQLAlchemy models rather than the Flask-SQLAlchemy magic, as
# it requires a global Flask app object and SQLAlchemy db object.
Base = declarative_base()


def main():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.update(
        #DB_CONNECTION_STRING=':memory:',
        CACHE_TYPE='simple',
        #SQLALCHEMY_DATABASE_URI='sqlite://',
    )
    app.debug = True

    injector = Injector([modules.AppModule(app)])
    views.configure_views(app=app, cached=injector.get(Cache).cached)
    FlaskInjector(app=app, injector=injector)
    app.run()
    #client = app.test_client()

    # response = client.get('/')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.post('/', data={'key': 'foo', 'value': 'bar'})
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.get('/')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.get('/hello')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.delete('/hello')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.get('/')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.get('/hello')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))
    # response = client.delete('/hello')
    # print('%s\n%s%s' % (response.status, response.headers, response.data))


if __name__ == '__main__':
    main()
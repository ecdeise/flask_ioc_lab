# import logging
#
# from injector import Module, Injector, inject, singleton
# from flask import Flask, Request, jsonify
# from flask_injector import FlaskInjector
# from flask_cache import Cache
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy import Column, String
#
# from .module import AppModule,
#
# il = logging.getLogger('injector')
# il.addHandler(logging.StreamHandler())
# il.level = logging.DEBUG
#
# Base = declarative_base()
#
#
#
# app = Flask(__name__)
# app.config.update(
#     DB_CONNECTION_STRING=':memory:',
#     CACHE_TYPE='simple',
#     SQLALCHEMY_DATABASE_URI='sqlite://',
# )
# app.debug = True
#
# injector = Injector([AppModule(app)])
# configure_views(app=app, cached=injector.get(Cache).cached)
#
# FlaskInjector(app=app, injector=injector)
# app.run()
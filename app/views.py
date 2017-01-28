from flask import Request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.orm.exc import NoResultFound

from app.models import KeyValue, User


def configure_views(app, cached):
    @app.route('/<key>')
    @inject(db=SQLAlchemy)
    def get(key, db):
        try:
            kv = db.session.query(KeyValue).filter(KeyValue.key == key).one()
        except NoResultFound:
            response = jsonify(status='No such key', context=key)
            response.status = '404 Not Found'
            return response
        return jsonify(key=kv.key, value=kv.value)

    @cached(timeout=1)
    @app.route('/')
    @inject(db=SQLAlchemy)
    def list(db):
        data = [i.key for i in db.session.query(KeyValue).order_by(KeyValue.key)]
        return jsonify(keys=data)

    @app.route('/', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def create(request, db):
        kv = KeyValue(request.form['key'], request.form['value'])
        db.session.add(kv)
        db.session.commit()
        response = jsonify(status='OK')
        response.status = '201 CREATED'
        return response

    @app.route('/<key>', methods=['DELETE'])
    @inject(db=SQLAlchemy)
    def delete(db, key):
        db.session.query(KeyValue).filter(KeyValue.key == key).delete()
        db.session.commit()
        response = jsonify(status='OK')
        response.status = '200 OK'
        return response

    @app.route('/index/<name>')
    @inject(request=Request)
    def index(request, name):
        response = 'index page ' + name
        return response

    @app.route('/user/<username>')
    @inject(db=SQLAlchemy)
    def getuser(db, username):
        try:
            user = db.session.query(User).filter(User.username == username).one()
        except NoResultFound:
            response = jsonify(status='No such user', context=username)
            response.status = '404 Not Found'
            return response
        return user.__repr__()


    @app.route('/user', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def addUser(request, db):
        user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        response = jsonify(status='OK')
        response.status = '201 CREATED'
        return response
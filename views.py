from functools import wraps

from flask import Request
from flask import flash
from flask import jsonify
from flask import render_template
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.orm.exc import NoResultFound
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms.ext.appengine.db import model_form

from models import KeyValue, User


def configure_views(app, cached):
    # @app.route('/<key>')
    # @inject(db=SQLAlchemy)
    # def get(key, db):
    #     try:
    #         kv = db.session.query(KeyValue).filter(KeyValue.key == key).one()
    #     except NoResultFound:
    #         response = jsonify(status='No such key', context=key)
    #         response.status = '404 Not Found'
    #         return response
    #     return jsonify(key=kv.key, value=kv.value)

    @cached(timeout=1)
    @app.route('/')
    @login_required
    def home():  # (request, db):

        print('index')
        return render_template('index.html')
        # if not session.get('logged_in'):
        #     session['logged_in'] = False
        #     return render_template('login.html')
        # else:
        #     return "hello admin"

    # def list(db):
    #     data = [i.key for i in db.session.query(KeyValue).order_by(KeyValue.key)]
    #     return jsonify(keys=data)

    @app.route('/login', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def do_admin_login(request, db):
        user = db.session.query(User).filter(User.username == request.form['username'] and User.password == request.form['password']).first()

        print(user)
        if user is None:
            flash('no user found')
        else:
            session['logged_in'] = user.is_authenticated
        return home()

        # if user is not None:
        #     if user.password == request.form['password']:
        #         session['logged_in'] = True
        #
        # if request.form['password'] == 'password' and request.form['username'] == 'admin':
        #     session['logged_in'] = True
        # else:
        #     flash('wrong password')
        # return home()

    # @app.route('/', methods=['POST'])
    # @inject(request=Request, db=SQLAlchemy)
    # def create(request, db):
    #     kv = KeyValue(request.form['key'], request.form['value'])
    #     db.session.add(kv)
    #     db.session.commit()
    #     response = jsonify(status='OK')
    #     response.status = '201 CREATED'
    #     return response

    # @app.route('/<key>', methods=['DELETE'])
    # @inject(db=SQLAlchemy)
    # def delete(db, key):
    #     db.session.query(KeyValue).filter(KeyValue.key == key).delete()
    #     db.session.commit()
    #     response = jsonify(status='OK')
    #     response.status = '200 OK'
    #     return response

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

    @app.route('/users')
    @inject(db=SQLAlchemy)
    def getusers(db):
        try:
            alluser = db.session.query(User).all()
        except NoResultFound:
            response = jsonify(status='No users')
            response.status = '404 Not Found'
            return response
        return alluser.__repr__()

    @app.route('/user', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def addUser(request, db):
        user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        response = jsonify(status='OK')
        response.status = '201 CREATED'
        return response

    @app.route('/edit_user/<id>', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def editUser(request, id):
        edit_form = model_form(User, Form)
        model = User.get(id);

        print(model)

        form = edit_form(request.form, model)
        print(form)

        # if form.validate_on_submit():
        #     form.populate_obj(model)
        #     model.put()
        #     print("User updated")
        #
        # return form

    @app.route('/react')
    def reacttest():
        return render_template('index.html')

    @app.route("/logout")
    def logout():
        session['logged_in'] = False
        return home()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return "<a href='/logout'>Logout</a>"
        return f(*args, **kwargs)

    return decorated_function

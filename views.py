from functools import wraps

from flask import Request
from flask import flash
from flask import jsonify
from flask import render_template
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from injector import inject
from sqlalchemy.orm.exc import NoResultFound
from views import *
from wtforms.ext.appengine.db import model_form

from flask import flash, request

from models import User, UserForm


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
        return render_template('index.html', auth=session.get('authenticated'))


    # def list(db):
    #     data = [i.key for i in db.session.query(KeyValue).order_by(KeyValue.key)]
    #     return jsonify(keys=data)

    @app.route('/login', methods=['POST'])
    @inject(request=Request, db=SQLAlchemy)
    def do_admin_login(request, db):
        user = db.session.query(User).filter(User.username == request.form['username'] and User.password == request.form['password']).first()
        if user is None:
            flash('no user found')
        else:
            session['authenticated'] = user.is_authenticated
        return home()

    @app.route('/sitemap')
    def list_routes():
        import urllib
        endpoints = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            endpoints.append(line)

        for line in sorted(endpoints):
            print (line)

        return render_template('sitemap.html', endpoints=endpoints, auth=session.get('authenticated'))

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
    @login_required
    @inject(db=SQLAlchemy)
    def getuser(db, username):

        if session.get('authenticated'):
            try:
                user = db.session.query(User).filter(User.username == username).one()
            except NoResultFound:
                response = jsonify(status='No such user', context=username)
                response.status = '404 Not Found'
                return response
            print(user.__repr__())
        return render_template('user.html', user=user, auth=session.get('authenticated'))


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

    @app.route('/user/edit/<id>/', methods=['GET', 'POST'])
    @inject(request=Request, db=SQLAlchemy)
    def edit_user(id, db, request):
        if session.get('authenticated'):
            user = db.session.query(User).filter(User.id == id).one()
            if user:
                form = UserForm(obj=user)
                form.populate_obj(user)

            return render_template('user.html', form = form)
        else:
            return render_template('login.html')


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
        #session['authenticated'] = False
        session.pop('authenticated', None)
        return home()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404


    # @app.route("/formtest", methods=['GET', 'POST'])
    # def formtest():
    #     form = ReusableForm(request.form)
    #
    #     print
    #     form.errors
    #     if request.method == 'POST':
    #         name = request.form['name']
    #         password = request.form['password']
    #         email = request.form['email']
    #         print
    #         name, " ", email, " ", password
    #
    #         if form.validate():
    #             # Save the comment here.
    #             flash('Thanks for registration ' + name)
    #         else:
    #             flash('Error: All the form fields are required. ')
    #
    #     return render_template('form_test.html', form=form)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #session.pop('authenticated')
        if not session.get('authenticated'):
            return render_template('login.html')
        # else:
        #     return "<a href='/logout'>Logout</a>"
        return f(*args, **kwargs)
    return decorated_function

from flask import render_template, url_for, redirect
from flask_security import login_required
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap

#from marketplace import admin

from marketplace import app
from marketplace.models import db, User, Category, Item

login = LoginManager(app)
Bootstrap(app)

categories_names_query = db.session.query(Category).all()


@login.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class LoginFrom(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegistrationFrom(FlaskForm):
    email = StringField('email' , validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(Category, db.session))
admin.add_view(MyModelView(Item, db.session))
admin.add_view(MyModelView(User, db.session))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(name=form.username.data).first()
        if user:
            if user.password == form.password.data:
                if form.username.data == 'Admin':
                    login_user(db.session.query(User).filter_by(name='Admin').first())
                    return redirect('/admin')
                return '<h1> You are logged in' + form.username.data + ' ' + form.password.data + '</h1>'

        return '<h1> Invalid username or password </h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form, categories=categories_names_query)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationFrom()

    if form.validate_on_submit():
        new_user = User(name=form.username.data, address=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return 'new user has been created'

    return render_template('signup.html', form=form, categories=categories_names_query)


@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out!'

@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    item_list = list()
    num = 0
    '''
        for category in db.session.query(Category).all():
        category_list.append(category.name)
        category_number += 1
        if category_number > 10:
            break
    '''
    #session = db.create_session()
    for item in db.session.query(Item).all():
        num += 1
        item_list.append({'title': item.title, 'description': item.description, 'id': num,
                          'item_id': item.item_id, 'price': item.price})
    db.session.close()

    #return render_template('list.html', category=category_list, advert=advert_list)
    return render_template('home_new.html', items=item_list, title='Все', categories=categories_names_query)


@app.route('/about')
def about():
    return render_template('about.html', title='About', categories=categories_names_query)


@app.route('/<int:post_id>')
def show_post(post_id):
    item_post_id = db.session.query(Item).filter(Item.id == post_id).first()
    return render_template('card_new.html', item=item_post_id, title='Выбранная оправа', categories=categories_names_query)


@app.route('/cat_<int:category>')
def show_category(category):
    category_query = db.session.query(Category).filter_by(id=category).first()
    return render_template('home_new.html', items=category_query.items, title=category_query.name, categories=categories_names_query)

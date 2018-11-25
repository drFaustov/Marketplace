from flask import Flask, render_template
from avito_db_entities import Category, Advert, User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import flask_login as login
import flask_admin as admin
import random
from flask_admin import expose
import avito_db as db

app = Flask(__name__)


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get_id(user_id)

class MyModelView(ModelView):
    def is_accessible(self):
        return random.randint(0,1)

class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

init_login()
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(MyModelView(Category, db.create_session()))
admin.add_view(MyModelView(Advert, db.create_session()))


@app.route('/list')
def c_list():
    category_number = 0
    category_list = list()
    advert_list = list()
    num = 0
    session = db.create_session()
    for category in session.query(Category).all():
        category_list.append(category.name)
        category_number += 1
        if category_number > 10:
            break
    for advert in session.query(Advert).all():
        num += 1
        advert_list.append({'title': advert.title, 'description': advert.description, 'id': num})
    return render_template('list.html', category=category_list, advert=advert_list)



@app.route('/post/<int:post_id>')
def show_post(post_id):
    advert_item = dict()
    num = 0
    session = db.create_session()
    for advert in session.query(Advert).all():
            num += 1
            if num == post_id:
                advert_item = {'title': advert.title, 'description': advert.description, 'id': num}
    return render_template('card.html', advert=advert_item)


if __name__ == '__main__':
    app.run()

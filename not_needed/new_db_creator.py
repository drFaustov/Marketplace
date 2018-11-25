from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_test.db'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=True)
    login = db.Column(db.String(100) , unique=True)
    password = db.Column(db.String(255))

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "\nUsers(user_id='{self.user_id}',\n" \
               "\t\t name='{self.name}')\n"\
               "\t\t phone='{self.phone}')\n"\
               "\t\t email='{self.email}')\n"\
               "\t\t login='{self.phone}')".format(self=self)

class Category(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    href = db.Column(db.String, nullable=True, unique=True)

    def __repr__(self):
        return "\nCategory(name='{self.name}',\n" \
               "\t\t href='{self.href}')".format(self=self)


class Advert(db.Model):
    advert_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    href = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    #price = Column(Integer)
    #category_id = Column(Integer, ForeignKey('categories.id'))
    #user_id = Column(Integer, ForeignKey('users.user_id'))

    def __repr__(self):
        return "\nAdvert(advert_id='{self.advert_id}',\n" \
               "\t\t title='{self.title}')\n"\
               "\t\t href='{self.href}')\n"\
               "\t\t description='{self.description}')".format(self=self)

if __name__ == '__main__':
    db.create_all()

    user_1 = User(name='Ivan', phone='+7123456789', email='ivan@example.ru', login='ivan_login', password='0')
    user_2 = User(name='Ivan1', phone='+7123456788', email='ivan1@example.ru', login='ivan1_login', password='1')

    advert_1 = Advert(title='adv1', href='http://', description='None')
    advert_2 = Advert(title='adv2', href='http://', description='None')

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(advert_1)
    db.session.add(advert_2)
    db.session.commit()

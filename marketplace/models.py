from datetime import datetime
from flask_login import UserMixin
from marketplace import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=True)
    login = db.Column(db.String(100) , unique=True)
    password = db.Column(db.String(255))

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "\nUsers(user_id='{self.user_id}',\n" \
               "\t\t name='{self.name}')\n"\
               "\t\t phone='{self.phone}')\n"\
               "\t\t address='{self.address}')".format(self=self)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    items = db.relationship('Item', backref='category')

    def __repr__(self):
        return "\nCategory(name='{self.name}')".format(self=self)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(50), index=True)
    image_href = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


    def __repr__(self):
        return "\nItem(item_id='{self.item_id}',\n" \
               "\t\t title='{self.title}')\n"\
               "\t\t image_href='{self.image_href}')\n" \
               "\t\t price='{self.price}')\n" \
               "\t\t description='{self.description}')".format(self=self)


class Advert(db.Model):
    __tablename__ = 'adverts'
    advert_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    href = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))

    #price = Column(Integer)
    #category_id = Column(Integer, ForeignKey('categories.id'))
    #user_id = Column(Integer, ForeignKey('users.user_id'))

    def __repr__(self):
        return "\nAdvert(advert_id='{self.advert_id}',\n" \
               "\t\t title='{self.title}')\n"\
               "\t\t href='{self.href}')\n"\
               "\t\t description='{self.description}')".format(self=self)


from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Enum, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

''' 
Database includes three entities of Category, Advert, User.
'''

# TODO: Check when databases are created if the current tables exists in order to avoid problems when new configuration
# TODO: of a table is introduced

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    name = Column(String(50), primary_key=True)
    href = Column(String, nullable=True, unique=True)

    def __repr__(self):
        return "\nCategory(name='{self.name}',\n" \
               "\t\t href='{self.href}')".format(self=self)


class Advert(Base):
    __tablename__ = 'adverts'
    advert_id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True)
    href = Column(String(255), nullable=False, unique=True)
    description = Column(String(255))

    #price = Column(Integer)
    #category_id = Column(Integer, ForeignKey('categories.id'))
    #user_id = Column(Integer, ForeignKey('users.user_id'))

    def __repr__(self):
        return "\nAdvert(advert_id='{self.advert_id}',\n" \
               "\t\t title='{self.title}')\n"\
               "\t\t href='{self.href}')\n"\
               "\t\t description='{self.description}')".format(self=self)


class User(Base, UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(255))
    created_on = Column(DateTime, nullable=True)
    login = Column(String(100) , unique=True)
    password = Column(String(255))

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "\nUsers(user_id='{self.user_id}',\n" \
               "\t\t name='{self.name}')\n"\
               "\t\t phone='{self.phone}')\n"\
               "\t\t address='{self.address}')".format(self=self)

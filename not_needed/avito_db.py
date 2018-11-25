#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from avito_db_entities import Base, Category, Advert

# start the DB engine
engine = create_engine('sqlite:///avito_adv_old.db', echo=True)

Session = sessionmaker(bind=engine, autocommit=True)


def create_session():
    session = Session()
    return session

Base.metadata.create_all(engine)

if __name__ == '__main__':
    Advert.__table__.drop(engine)
    session.add(Advert(advert_id='1', title='hello', href='_', description='akjfhaskhf'))
    session.commit()

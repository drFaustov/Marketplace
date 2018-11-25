from avito_db_entities import Category, User, Advert
import avito_db as db

if __name__ == '__main__':
    category_list = list()
    advert_list = list()

    for category in db.session.query(Category).all():
        category_list.append(category.name)

    print(category_list, '\n')

    for advert in db.session.query(Advert).all():
        advert_list.append(advert.title)

    print(advert_list, '\n')
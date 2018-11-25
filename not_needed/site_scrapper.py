import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from avito_db_entities import Category, User, Advert
import avito_db as db

if __name__ == '__main__':

    ''' 
    The block of code below gets the main page from avito.ru/moskva.
    It parses all categories and their hrefs from the site.
    '''

    # get the front page of avito
    url = 'https://www.avito.ru/moskva/'
    site_request = requests.get(url)

    with open('http_request_main_page.html', 'w', encoding='utf-8') as output_file:
        output_file.write(site_request.text)

    soup = BeautifulSoup(site_request.text, features='lxml')

    # fetch all category attributes and tags with hyperlinks
    categories_tags = soup.find('div', {'class': 'form-select-v2'}).find_all('option')
    category_htags = soup.find('nav', {'class': 'category-map'}).find_all('a')

    # creating a dict of references
    category_href = dict()
    for category_htag in category_htags:
        category_href[re.sub('\n ', '', category_htag.text)] = category_htag.get('href')

    # adding categories and their hrefs to the database
    category_dict = dict()
    for category in categories_tags:
        category_dict[category.get('value')] = category.text
        # add to db
        if not db.session.query(Category).filter(Category.name == category.text).first():
            try:
                db.session.add(Category(name=category.text,
                                        href=category_href[category.text]))
            except KeyError:
                db.session.add(Category(name=category.text,
                                        href=''))

    db.session.commit()
    #print(db.session.query(Category).all())

    ''' The code below allows a user to search a wanted item in a certain category '''

    # choice of category and item to look for
    search_category = 'Одежда'  #input('Please enter category:')

    # item to search
    search_item = 'очки'    #imput('Please enter an item you are looking for:')

    # appending a url for search
    item_reference_url = '?s_trg=3&q=' + search_item

    search_category_href = db.session.query(Category).filter(Category.name.like('%'+search_category+'%')).first().href
    url_item = urljoin(url, search_category_href + item_reference_url)

    ''' The code below allows a user to parse all the found items into a database '''

    # request for search for the item in the chosen category
    soup_item = BeautifulSoup(requests.get(url_item).text, features="lxml")

    item_table = soup_item.find('div', {'class': 'catalog-content'})
    #item_advs = item_table.find_all('div', {'class': 'item item_table clearfix js-catalog-item-enum js-item-extended '
    #                                     'item_table_extended snippet-experiment item-new-highlight '
    #                                     'item_hide-elements'})
    item_advs = item_table.find_all('div', {'itemtype': "http://schema.org/Product"})

    # TODO: make a module with a get_category, get_searched_items, update_data_base functions
    i = 0
    for adv in item_advs:
        i += 1
        print(i)
        # get all information from the list of item_advs
        adv_id = adv.get('data-item-id')
        adv_description = adv.find('meta').get('content')
        try:
            adv_href = adv.find('a', {'class': 'js-item-slider item-slider large-picture'}).get('href')
        except AttributeError:
            continue
        adv_soup = BeautifulSoup(requests.get(urljoin(url, adv_href)).text, features="lxml")

        adv_title = adv_soup.find('span', {'class': 'title-info-title-text'}).text

        if not db.session.query(Advert).filter(Advert.advert_id == adv_id).first():
            db.session.add(Advert(advert_id=adv_id,
                                  title=adv_title,
                                  href=adv_href,
                                  description=adv_description))


    db.session.commit()
    print(db.session.query(Advert).all())




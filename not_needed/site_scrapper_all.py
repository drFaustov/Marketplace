import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from avito_db_entities import Category, User, Item
import avito_db as db

if __name__ == '__main__':

    ''' 
    The block of code below gets the main page from avito.ru/moskva.
    It parses all categories and their hrefs from the site.
    '''

    # get the front page of avito

    avito = False

    if avito:

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

    url_glasses = ['https://www.partyof2two.com/zjenskie',
                   'https://www.partyof2two.com/muzjkie',
                   'https://www.partyof2two.com/uniseks',
                   'https://www.partyof2two.com/kids']


    ''' The code below allows a user to parse all the found items into a database '''

    # request for search for the item in the chosen category

    item_req = requests.get(url_glasses).text
    with open('http_request_main_page.html', 'w', encoding='utf-8') as output_file:
            output_file.write(item_req)

    soup_item = BeautifulSoup(item_req, features="lxml")

    item_groups = soup_item.find_all('div', {'class': 't754'})
    #item_advs = item_table.find_all('div', {'class': 'item item_table clearfix js-catalog-item-enum js-item-extended '
    #                                     'item_table_extended snippet-experiment item-new-highlight '
    #                                     'item_hide-elements'})
    #item_groups = items_container_html.find_all('div', {'class': 't754'})

    i = 0
    for group in item_groups:

        items = group.find_all('div', {'class': 't754__col t-col t-col_4 t-align_center t-item t754__col_mobile-grid js-product'})

        # TODO: make a module with a get_category, get_searched_items, update_data_base functions
        for item in items:
            i += 1
            print(i)
            # get all information from the list of item_advs
            try:
                item_id = item.get('data-product-lid')
                item_title = item.find('div', {'class': 't754__title t-name t-name_md js-product-name'}).text

                item_img_1 = item.find('div', {'class': 't754__bgimg t754__bgimg_first_hover t-bgimg js-product-img'}).get('data-original')
                item_img_2 = item.find('div', {'class': 't754__bgimg t754__bgimg_second t-bgimg'}).get('data-original')

            except AttributeError:
                continue

            # download the url contents in binary format
            item_image_req = requests.get(item_img_1)

            # open method to open a file on your system and write the contents
            with open('imgs/img_{}_1.jpg'.format(item_id), 'wb') as code:
                code.write(item_image_req.content)

            item_image_req = requests.get(item_img_2)

            # open method to open a file on your system and write the contents
            with open('imgs/img_{}_2.jpg'.format(item_id), 'wb') as code:
                code.write(item_image_req.content)

            try:
                item_price = item.find('div', {'class': 't754__price-value js-product-price'}).text

                item_popup = soup_item.find('div', {'class': 't-popup'})\
                                      .find('div', {'id': 't754__product-{}'.format(item_id)})

                item_description = item_popup.find('div', {'class': 't754__descr t-descr t-descr_xxs'}).text

            except AttributeError:
                item_price = None
                item_popup = None
                item_description = None

            if not db.session.query(Item).filter(Item.item_id == item_id).first():
                db.session.add(Item(item_id=item_id,
                                    title=item_title,
                                    image_href=item_img_1,
                                    price=item_price,
                                    description=item_description))
            db.session.commit()

    print(db.session.query(Item).all())




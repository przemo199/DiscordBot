"""This module is used to pull information from www.amazon.uk"""

import io

import requests
from lxml import etree

search_url = 'https://www.amazon.co.uk/s?k='

name_xpath = '//*[@id="productTitle"]/text()'
price_xpath = '//*[@id="priceblock_ourprice"]/text()'
altprice_xpath = '//*[@id="priceblock_saleprice"]/text()'
otherprice_xpath = '//*[@id="olp-upd-new-used"]/span/a/span[3]/text()'
rating_xpath = '//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span/text()'
reviews_xpath = '//*[@id="acrCustomerReviewText"]/text()'
delivery_xpath = '//*[@id="price-shipping-message"]/span/b/text()'
altdelivery_xpath = '//*[@id="price-shipping-message"]/b/text()'


def main(search_term):
    request_url = search_url + search_term

    response = requests.get(request_url)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    games_parent_path = name_xpath + '/div[1]'
    games_parent = html.xpath(games_parent_path)

    games_found = 'emptyProvider' not in games_parent[0].get('class')

    if games_found:
        games = html.xpath(games_parent_path + '/div[1]')
        number_of_games_found = len(games[0].getchildren())

        number_of_games_to_return = number_of_games_found
        if number_of_games_to_return > 5:
            number_of_games_to_return = 5

        return_list = []
        for x in range(number_of_games_to_return):
            url = 'https://gg.deals' + games[0][x][0].get('href')
            return_list.append(getdetails(url))
        return return_list
    return False


def getdetails(product_url):
    response = requests.get(product_url)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    product_name = html.xpath(name_xpath)
    product_name = processlist(product_name)

    product_price = html.xpath(price_xpath)
    product_price = processlist(product_price)

    if product_price == '-':
        product_price = html.xpath(altprice_xpath)
        product_price = processlist(product_price)

    other_price = html.xpath(otherprice_xpath)
    other_price = processlist(other_price)

    product_rating = html.xpath(rating_xpath)
    product_rating = processlist(product_rating)

    product_reviews = html.xpath(reviews_xpath)
    product_reviews = processlist(product_reviews)

    delivery = html.xpath(delivery_xpath)
    delivery = processlist(delivery)

    if delivery == '-':
        delivery = html.xpath(altdelivery_xpath)
        delivery = processlist(delivery)

    return product_name, product_price, other_price, product_rating, product_reviews, delivery


def processlist(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value


print(getdetails('https://www.amazon.co.uk/Logitech-LIGHTSPEED-Pro-Grade-Adjustable-Programmable/dp/B07S9DR8QG/'))

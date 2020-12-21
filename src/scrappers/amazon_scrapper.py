"""This module is used to pull information from www.amazon.uk"""
# TODO: select all elements with data-index convert to string and with shortlink_regex get links to sepcific products
import io
import re

import requests
from lxml import etree

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept-Language': 'en-UK, en;q=0.5'})

base_url = 'https://www.amazon.co.uk'
search_url = 'https://www.amazon.co.uk/s?k='

name_xpath = '//*[@id="productTitle"]/text()'
price_xpath = '//*[@id="priceblock_ourprice"]/text()'
altprice_xpath = '//*[@id="priceblock_saleprice"]/text()'
otherprice_xpath = '//*[@id="olp-upd-new-used"]/span/a/span[3]/text()'
rating_xpath = '//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span/text()'
reviews_xpath = '//*[@id="acrCustomerReviewText"]/text()'
delivery_xpath = '//*[@id="price-shipping-message"]/span/b/text()'
altdelivery_xpath = '//*[@id="price-shipping-message"]/b/text()'

productlink_xpath = '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[2]/div/span/div/div/div[2]/div[1]/div/div/span/a'

link_regex = r'\/.*\/dp\/.*\/'
shortlink_regex = r'\/dp\/.{10}'


def searchforproduct(search_term):
    request_url = search_url + search_term

    response = requests.get(request_url, headers = HEADERS)
    response = response.text
    htmlparser = etree.HTMLParser()
    html_tree = etree.parse(io.StringIO(response), htmlparser)

    hrefs = html_tree.xpath('//*[@data-index]//span[@class="rush-component"]//a[@class="a-link-normal"]/@href')

    elems = html_tree.xpath('//*[@data-index]//span[@class="rush-component"]')

    unique = []
    for i in elems:
        a = re.findall(shortlink_regex, str(etree.tostring(i)))
        print(a)
        # if a.group(0) and a.group(0) not in unique:
        # unique.append(a.group(0))

    print(unique)

    links = []
    for link in hrefs:
        links.append(re.search(link_regex, link).group(0))

    # only take unique elements from links
    unique_links = []
    for link in links:
        if link not in unique_links:
            unique_links.append(link)

    for i in range(len(unique_links)):
        unique_links[i] = base_url + unique_links[i]

    return unique_links


def getdetails(product_url):
    response = requests.get(product_url, headers = HEADERS)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    product_name = html.xpath(name_xpath)
    product_name = processdetail(product_name)

    product_price = html.xpath(price_xpath)
    product_price = processdetail(product_price)

    other_price = html.xpath(otherprice_xpath)
    other_price = processdetail(other_price)

    product_rating = html.xpath(rating_xpath)
    product_rating = processdetail(product_rating)

    product_reviews = html.xpath(reviews_xpath)
    product_reviews = processdetail(product_reviews)

    delivery = html.xpath(delivery_xpath)
    delivery = processdetail(delivery)

    if delivery == '-':
        delivery = html.xpath(altdelivery_xpath)
        delivery = processdetail(delivery)

    if product_price == '-':
        product_price = html.xpath(altprice_xpath)
        product_price = processdetail(product_price)

    return product_name, product_price, other_price, product_rating, product_reviews, delivery


def processdetail(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value


print(searchforproduct('tv+stick'))

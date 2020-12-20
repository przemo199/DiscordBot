import io

import requests
from lxml import etree

url1 = 'https://gg.deals/gb/game/mars-horizon/'
title_xpath = '//*[@id="page"]/div[2]/div/ul/li[4]/a/span/text()'
store_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[1]/a/div/span/span/text()'
keyshop_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[2]/a/div/span/span/text()'


def getprices(url):
    response = requests.get(url)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    title = html.xpath(title_xpath)
    store_price = html.xpath(store_xpath)
    keyshop_price = html.xpath(keyshop_xpath)

    return title[0], store_price[0], keyshop_price[0]


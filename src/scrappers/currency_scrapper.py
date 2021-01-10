"""This module is used to scrap currency exchange rates from web"""

import io

import requests
from lxml import etree

USER_AGENT = ({'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
               'Accept-Language': 'en-UK, en;q=0.5'})

EXCHANGE_URL_HEAD = 'https://uk.finance.yahoo.com/quote/'
EXCHANGE_URL_TAIL = '%3DX'

EXCHANGE_XPATH = '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()'
TIME_INFO_XPATH = '//*[@id="quote-market-notice"]/span/text()'
CLOSE_XPATH = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()'
OPEN_XPATH = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span/text()'
YEAR_RANGE_XPATH = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/text()'


def getdetails(query):
    query = query.split()
    exchange_url = EXCHANGE_URL_HEAD + query[0] + query[2] + EXCHANGE_URL_TAIL
    response = requests.get(exchange_url, headers=USER_AGENT)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    exchange_rate = html.xpath(EXCHANGE_XPATH)
    exchange_rate = processdetail(exchange_rate)

    market_info = html.xpath(TIME_INFO_XPATH)
    market_info = processdetail(market_info)

    close_price = html.xpath(CLOSE_XPATH)
    close_price = processdetail(close_price)

    open_price = html.xpath(OPEN_XPATH)
    open_price = processdetail(open_price)

    year_range = html.xpath(YEAR_RANGE_XPATH)
    year_range = processdetail(year_range)

    return [exchange_rate, market_info, close_price, open_price, year_range]


def processdetail(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value

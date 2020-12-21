"""This module is used to scrap currency exchange rates from web"""

import io

import requests
from lxml import etree

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept-Language': 'en-UK, en;q=0.5'})

url_head = 'https://uk.finance.yahoo.com/quote/'
url_tail = '%3DX'

yahooexchange_xpath = '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()'
yahooinfo_xpath = '//*[@id="quote-market-notice"]/span/text()'
yahooclose_xpath = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()'
yahooopen_xpath = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span/text()'
yahooyearrange_xpath = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/text()'


def getdetails(query):
    query = query.split()
    exchange_url = url_head + query[0] + query[2] + url_tail
    response = requests.get(exchange_url, headers = HEADERS)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    exchange_rate = html.xpath(yahooexchange_xpath)
    exchange_rate = processdetail(exchange_rate)

    market_info = html.xpath(yahooinfo_xpath)
    market_info = processdetail(market_info)

    close_price = html.xpath(yahooclose_xpath)
    close_price = processdetail(close_price)

    open_price = html.xpath(yahooopen_xpath)
    open_price = processdetail(open_price)

    year_range = html.xpath(yahooyearrange_xpath)
    year_range = processdetail(year_range)

    return [exchange_rate, market_info, close_price, open_price, year_range]


def processdetail(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value

"""This module is used to pull information from www.gg.deals"""

import io

import requests
from lxml import etree

SEARCH_URL = 'https://gg.deals/games/?title='
TITLE_XPATH = '//*[@id="page"]/div[2]/div/ul/li[4]/a/span/text()'
STORE_PRICE_XPATH = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[1]/a/div/span/span/text()'
KEYSHOP_PRICE_XPATH = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[2]/a/div/span/span/text()'
METASCORE_XPATH = '//*[@id="game-info-side"]/div[3]/div/div/div[1]/a/span/span/text()'
USERSCORE_XPATH = '//*[@id="game-info-side"]/div[3]/div/div[1]/div[2]/a/span/span/text()'

LIST_OF_GAMES_XPATH = '//*[@id="games-list"]/div[1]'


def searchforgame(search_term):
    request_url = SEARCH_URL + search_term

    response = requests.get(request_url)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    games_parent = html.xpath(LIST_OF_GAMES_XPATH)

    games_found = 'emptyProvider' not in games_parent[0].get('class')

    if games_found:
        games = html.xpath(LIST_OF_GAMES_XPATH)
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


def getdetails(game_url):
    response = requests.get(game_url)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    game_title = html.xpath(TITLE_XPATH)
    game_title = processdetail(game_title)

    store_price = html.xpath(STORE_PRICE_XPATH)
    store_price = processdetail(store_price)

    keyshop_price = html.xpath(KEYSHOP_PRICE_XPATH)
    keyshop_price = processdetail(keyshop_price)

    metascore = html.xpath(METASCORE_XPATH)
    metascore = processdetail(metascore)

    userscore = html.xpath(USERSCORE_XPATH)
    userscore = processdetail(userscore)

    return game_title, store_price, keyshop_price, metascore, userscore, game_url


def processdetail(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value

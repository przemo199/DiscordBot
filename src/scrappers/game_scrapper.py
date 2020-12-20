"""This module is used to pull information from www.gg.deals"""

import io

import requests
from lxml import etree

search_url = 'https://gg.deals/games/?title='
title_xpath = '//*[@id="page"]/div[2]/div/ul/li[4]/a/span/text()'
store_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[1]/a/div/span/span/text()'
keyshop_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[2]/a/div/span/span/text()'
games_list_xpath = '//*[@id="games-list"]'


def main(search_term):
    request_url = search_url + search_term

    response = requests.get(request_url)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    games_parent_path = games_list_xpath + '/div[1]'
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


def getdetails(game_url):
    response = requests.get(game_url)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    game_title = html.xpath(title_xpath)
    store_price = html.xpath(store_xpath)
    keyshop_price = html.xpath(keyshop_xpath)

    game_title = processlist(game_title)
    store_price = processlist(store_price)
    keyshop_price = processlist(keyshop_price)

    return game_title, store_price, keyshop_price


def processlist(value):
    if len(value) == 0:
        value = '-'
    else:
        value = str(value[0]).strip()
    return value

import io

import requests
from lxml import etree

url1 = 'https://gg.deals/games/?title='
title_xpath = '//*[@id="page"]/div[2]/div/ul/li[4]/a/span/text()'
store_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[1]/a/div/span/span/text()'
keyshop_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[2]/a/div/span/span/text()'

gamesList_xpath = '//*[@id="games-list"]'

def main(search_term):
    search_url = url1 + search_term

    response = requests.get(search_url)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    games_parent_path = gamesList_xpath + '/div[1]'
    games_parent = html.xpath(games_parent_path)

    games_found = 'emptyProvider' not in games_parent[0].get('class')
    
    if games_found:
        games = html.xpath(games_parent_path+'/div[1]')
        number_of_games_found = len(games[0].getchildren())

        number_of_games_to_return = number_of_games_found
        if number_of_games_to_return > 5:
            number_of_games_to_return = 5
        
        return_list = []
        for x in range(number_of_games_to_return):
            url = 'https://gg.deals' + games[0][x][0].get('href')
            return_list.append(getprices(url))
        return return_list
    return False
    
def getprices(url):
    response = requests.get(url)
    response = response.text

    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    title = html.xpath(title_xpath)
    store_price = html.xpath(store_xpath)
    keyshop_price = html.xpath(keyshop_xpath)

    return title[0], store_price[0], keyshop_price[0]

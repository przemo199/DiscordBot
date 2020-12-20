import io

import requests
from lxml import etree

url1 = 'https://gg.deals/games/?title='
title_xpath = '//*[@id="page"]/div[2]/div/ul/li[4]/a/span/text()'
store_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[1]/a/div/span/span/text()'
keyshop_xpath = '//*[@id="game-card"]/div[1]/div/div[2]/div[2]/div/div[2]/a/div/span/span/text()'

gamesList_xpath = '//*[@id="games-list"]'

def main(searchTerm):
    searchUrl = url1 + searchTerm

    response = requests.get(searchUrl)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    gamesParentPath = gamesList_xpath + '/div[1]'
    gamesParent = html.xpath(gamesParentPath)

    gamesFound = 'emptyProvider' not in gamesParent[0].get('class')
    
    if gamesFound:
        games = html.xpath(gamesParentPath+'/div[1]')
        numberOfGamesFound = len(games[0].getchildren())

        number_of_games_to_return = numberOfGamesFound
        if number_of_games_to_return > 5:
            number_of_games_to_return = 5
        
        returnList = []
        for x in range(number_of_games_to_return):
            url = 'https://gg.deals' + games[0][x][0].get('href')
            values = getprices(url)
            returnList.append(getprices(url))
        return returnList
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


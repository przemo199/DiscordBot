"""This module is used to pull information from websites"""

import io

import requests
from lxml import etree

base_url = 'https://www.newegg.com/p/pl?d='
error_xpath = '//*[@id="app"]/div[2]/section/div/div/div[2]/div/div/div/div[2]/div/div[1]/p/span'
item_list_xpath = '//*[@class="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell"]'
name_xpath = '//*[@class="item-title"]'
rating_xpath = '//*[@class="item-rating"]'
rating_num_xpath = '//*[@class="item-rating-num"]'
price_xpath = '//*[@class="price-current "]'

def main(search_term):
    search_url = base_url + search_term

    response = requests.get(search_url)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)

    items_found = len(html.xpath(error_xpath)) == 0

    if items_found:
        num_items_to_display = min(5,len(html.xpath(item_list_xpath)[0].getchildren()))
    
        return_list = []
        for x in range(num_items_to_display):
            name = html.xpath(item_list_xpath + f'/div[{x+1}]' + name_xpath)#[0].text
            rating = html.xpath(item_list_xpath + f'/div[{x+1}]' + rating_xpath)#[0].get('title')[-1]
            rating_num = html.xpath(item_list_xpath + f'/div[{x+1}]' + rating_num_xpath)#[0].text[1]
            price_strong = html.xpath(item_list_xpath + f'/div[{x+1}]' + price_xpath + '/strong')#[0].text
            price_sup = html.xpath(item_list_xpath + f'/div[{x+1}]' + price_xpath + '/sup')#[0].text

            item = []
            if name:item.append(name[0].text)
            else:item.append(None)
            if rating:item.append(rating[0].get('title')[-1])
            else:item.append(None)
            if rating_num:item.append(rating_num[0].text[1])
            else:item.append(None)
            if price_strong: item.append(price_strong[0].text + price_sup[0].text)
            else:item.append(None)
            return_list.append(item)
        return return_list
    return False

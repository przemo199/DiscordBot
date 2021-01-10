"""This module is used to scrap popular user agents"""

import io
import random

import requests
from lxml import etree

WEBSITE_URL = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'

USER_AGENT_XPATH = '//td/a/text()'


class UserAgents:
    def __init__(self):
        self.user_agents = getuseragents()

    def getagent(self):
        return random.choice(self.user_agents)


def getuseragents():
    response = requests.get(WEBSITE_URL)
    response = response.text
    htmlparser = etree.HTMLParser()
    html = etree.parse(io.StringIO(response), htmlparser)
    user_agents = html.xpath(USER_AGENT_XPATH)

    return user_agents

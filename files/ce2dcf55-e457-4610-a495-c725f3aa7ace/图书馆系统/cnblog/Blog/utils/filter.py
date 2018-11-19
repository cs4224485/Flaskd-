# Author: harry.cai
# DATE: 2018/7/9
from bs4 import BeautifulSoup


def filter_js(content):
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup.find_all():
        if tag.name == 'script':
            tag.decompose()
    return soup

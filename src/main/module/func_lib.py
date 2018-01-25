# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from konlpy.tag import Kkma
from konlpy.utils import pprint



from html2text import html2text
import re
from konlpy.tag import Twitter; t = Twitter()

# 클리닝 함수
def clean_text(text):

    cleaned_text = re.sub('[0-9]', '', text)
    return cleaned_text


# crawling and analyse
def crw(url):

    #crawling!!
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    soup = unicode(soup)
    text = html2text(soup)
    text = text.encode('utf-8')

    # removing meanless number
    text = clean_text(text)

    # make twitter class
    kkma = Twitter()
    t1 = kkma.nouns(text)
    return t1






#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import urllib
import sys


url = str(sys.argv[1])
r = urllib.urlopen(url).read()
soup = bs(r, "lxml")
# print(soup.prettify().encode('utf-8'))
# looking for div class="fb_content clearfix " id="content"
fourDiv = soup.find_all("div", class_="fb_content clearfix ")
if ("not found" in str(fourDiv)):
    print("Page does not exist")
else:
    print("Page exists")

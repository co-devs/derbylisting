#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import urllib
import argparse


def badURL(url):
    if args.test:
        return '0'
    else:
        return str(url).strip('\n') + ' does not exist'


def goodURL(url):
    if args.test:
        return '1'
    else:
        return str(url).strip('\n') + ' exists'

def questionURL(url):
    if args.test:
        return '-1'
    else:
        return str(url).strip('\n') + ' is questionable.  Manually check.'


def fixURL(url):
    if "http" not in str(url):
        return "http://" + url
    else:
        return url


def idURL(url, r):
    if "facebook" not in str(url):
        if args.test:
            print(goodURL(url))
        else:
            print(goodURL(url))
    else:
        testFacebookURL(url, r)


def testFacebookURL(url, r):
    soup = bs(r, "lxml")
    # Need to be logged in (probably a group)
    haltDiv = soup.find_all("div", class_="_585r")
    # print haltDiv
    fourDiv = soup.find_all("div", class_="fb_content clearfix ")
    # print soup.prettify().encode('utf-8')
    if ("You must log in to continue" in str(haltDiv)):
        print(questionURL(url))
    # Don't need to be logged in (probably not group)
    # looking for div class="fb_content clearfix " id="content"
    elif ("not found" in str(fourDiv)):
        # print("Page does not exist")
        print(badURL(url))
    else:
        # print("Page exists")
        print(goodURL(url))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Return whether or not a page exists.
                                     ALPHA BUILD.  Currently only checks
                                     facebook URLS.  Intend to look into mySQL
                                     support.""")
    parser.add_argument('-u', '--urls', metavar='URL', nargs='+',
                        help='URL(s) to check')
    parser.add_argument('-f', '--file', metavar='File',
                        help='File of URLs, one per line')
    parser.add_argument('-t', '--test', action='store_true',
                        help="""test flag, does not return friendly output.  1 =
                        URL exists, 0 = does not exist, -1 = manual check.
                        Intend to implement output to file option, with choice
                        to output based on code.""")
    args = parser.parse_args()
    if args.urls:
        for url in args.urls:
            try:
                r = urllib.urlopen(fixURL(url))
            except Exception:
                # print(url + ' is bad URL, could not open')
                print(badURL(url))
                continue
            idURL(url, r)
    elif args.file:
        try:
            f = open(args.file, "r")
        except:
            print("Invalid file")
            raise SystemExit
        urls = f.readlines()
        f.close()
        for url in urls:
            # print str(url).strip('\n')
            try:
                r = urllib.urlopen(fixURL(url))
            except Exception:
                # print(url + ' is bad URL, could not open')
                print(badURL(url))
                continue
            idURL(url, r)

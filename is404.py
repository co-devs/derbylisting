#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import urllib
import argparse
import os.path


def badURL(url):
    # If we are not suppressing bad url output
    if not args.suppress_bad_urls:
        # If test flag present
        if args.test:
            # Return code 0
            return '0'
        else:
            # Else return proper string
            return str(url).strip('\n') + ' does not exist'
    # If we are suppressing
    else:
        # Return None
        return None


def goodURL(url):
    # If we are not suppressing good url output
    if not args.suppress_good_urls:
        # If test flag present
        if args.test:
            # Return code 1
            return '1'
        else:
            # Else return proper string
            return str(url).strip('\n') + ' exists'
    # If we are suppressing
    else:
        # Return None
        return None


def questionURL(url):
    # If we are not suppressing questionable url output
    if not args.suppress_question_urls:
        # If test flag present
        if args.test:
            # Return code -1
            return '-1'
        else:
            # Else return proper string
            return str(url).strip('\n') + ' is questionable.  Manually check.'
    # If we are suppressing
    else:
        # Return None
        return None


def fixURL(url):
    # Check to see if URL contains http
    if "http" not in str(url):
        # If it is not, then prepend it and return
        return "http://" + url
    else:
        # If it is then return plain URL
        return url


def idURL(url, r):
    # Identify the kind of site
    if "facebook" not in str(url):
        # If not a facebook page, and page opened,
        # We are currently ASSUMING that the page is good
        outputResponse(handleResponse(url, 'good'))
    else:
        # If facebook, test it
        testFacebookURL(url, r)


def testFacebookURL(url, r):
    soup = bs(r, "lxml")
    # Get div containing text that indicates page behind a login screen
    haltDiv = soup.find_all("div", class_="_585r")
    # Get div containing page does not exist
    fourDiv = soup.find_all("div", class_="fb_content clearfix ")
    # If the div that would contain login error text exists
    if ("You must log in to continue" in str(haltDiv)):
        # Then pring questionable URL.  We can't check it w/o logging in
        outputResponse(handleResponse(url, 'question'))
    # Else, if we don't need to log in but get a facebook 404
    elif ("not found" in str(fourDiv)):
        # Then the page does not exist
        outputResponse(handleResponse(url, 'bad'))
    else:
        # Otherwise, the facebook page probably exists
        outputResponse(handleResponse(url, 'good'))


def handleURLs(urls):
    # For each URL in list urls
    for url in urls:
        # Try to open the url
        try:
            r = urllib.urlopen(fixURL(url))
        # If the URL cannot be opened, handle bad response
        except Exception:
            outputResponse(handleResponse(url, 'bad'))
            # Move to next URL in list or quit if at end
            continue
        # If URL is good, identify it with idURL()
        idURL(url, r)


def handleResponse(url, status):
    # If bad URL and not suppressed, then call badURL() and return response
    if status.lower() == 'bad':
        response = badURL(url)
        if response:
            return response
    # # If good URL and not suppressed, then call goodURL() and return response
    elif status.lower() == 'good':
        response = goodURL(url)
        if response:
            return response
    # If question URL and not suppressed, then call questionURL() and
    # return response
    elif status.lower() == 'question':
        response = questionURL(url)
        if response:
            return response
    else:
        return 'Error in handleResponse'


def outputResponse(response):
    # If output to file flag is set
    if args.output:
        # Open file to append response
        f = open(args.output, 'a+')
        # Append response
        f.write(response + '\n')
    else:
        # print response to terminal.  Probably some unnecessary repetition of
        # if response: here since it's also in handleResponse()
        if response:
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Return whether or not a page exists.
                                     ALPHA BUILD.  Currently only checks
                                     facebook URLS.  Intend to look into mySQL
                                     support.""")
    parser.add_argument('-u', '--urls', metavar='URL', nargs='+',
                        help='URL(s) to check')
    parser.add_argument('-f', '--file', metavar='File',
                        help='File of URLs, one per line')
    parser.add_argument('-G', '--suppress-good-urls', action='store_true',
                        default=False,
                        help='Do not print good URLs')
    parser.add_argument('-B', '--suppress-bad-urls', action='store_true',
                        default=False,
                        help='Do not print bad URLs')
    parser.add_argument('-Q', '--suppress-question-urls', action='store_true',
                        default=False,
                        help='Do not print questionable URLs')
    parser.add_argument('-o', '--output', metavar='File',
                        help='Print results to file')
    parser.add_argument('-m', '--mysql', metavar='mySQL',
                        help='output in MySQL command format')
    parser.add_argument('-t', '--test', action='store_true',
                        help="""test flag, does not return friendly output.  1 =
                        URL exists, 0 = does not exist, -1 = manual check.
                        Intend to implement output to file option, with choice
                        to output based on code.""")
    args = parser.parse_args()
    # If provided a list of URLs in command line
    if args.output:
        if os.path.isfile(args.output):
            print('Error, file exists. Please enter a new file name')
            raise SystemExit
    if args.urls:
        # Call handleURLs() on list
        handleURLs(args.urls)
    # Else if provided a file with URLs
    elif args.file:
        try:
            # Try to open the file
            f = open(args.file, "r")
        except Exception:
            # If it fails, return error and exit
            print("Invalid file")
            raise SystemExit
        # If the file can be opened, read its lines
        urls = f.readlines()
        # Close file
        f.close()
        # Call handleURLs() on list
        handleURLs(urls)

#!/usr/bin/python3


import sys
import csv
from lxml import html
import requests
import re


# XPATHs


XPATH = {
    'ID': 'string(./@data-post-id)',
    'IP': 'string(./div[@class="comment-date"])',
    'Date': 'string(./div[@class="comment-date"])',
    'Time': 'string(./div[@class="comment-date"])',
    'Name': 'string(./div[@class="comment-author"])',
    'Comment': 'string(./div/div[@class="comment-content-inner"])',
    'Up': 'string(.//div[@class="comment-votes-up"]//span[@class="comment-votes-count"])',
    'Down': 'string(.//div[@class="comment-votes-down"]//span[@class="comment-votes-count"])'
    }


# Regexes


regex = {
    'IP': re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
    'Date': re.compile('\d{4}-\d{1,2}-\d{1,2}'),
    'Time': re.compile('\d{2}:\d{2}')
}


# Substitutions


subs = {
    'Name': '[\t\n]',
    'Comment': '[\t\n]',
    }


# Functions


def single_comment_parse(comment):
    new_line = dict()

    for field in XPATH.keys():
            try:
                raw = comment.xpath(XPATH[field])
                if field in regex.keys():
                    raw = regex[field].findall(raw)[0]
                if field in subs.keys():
                    raw = re.sub(subs[field], '', raw)
                new_line[field] = raw
            except:
                pass

    return new_line


def whole_page_parse(tree):
    main_list = list()

    for comment in tree.xpath('//div[@data-post-id!=""]'):
        main_list.append(single_comment_parse(comment))

    return main_list


def next_url(tree):
    if tree.xpath('//a[@class="comments-pager-arrow-last"]/@href'):
        return tree.xpath('//a[@class="comments-pager-arrow-last"]/@href')[0]
    else:
        return 0
    
    
def single_url_scraper(url):
    
    main_list = list()
    
    page = requests.get(url)
    while page.status_code == 200:
        tree = html.fromstring(page.content.decode('utf-8'))

        main_list = main_list + whole_page_parse(tree)

        if next_url(tree):
            page = requests.get(next_url(tree))
        else:
            break
    
    return main_list


if __name__ == '__main__':

    url = sys.argv[1]
    outfile = re.findall('=(\d+)$', url)[0] + '.csv'

    s = 2
    reg = 0
    url = url + '&com=1' + '&reg=' + str(reg) + '&s=' + str(s) + '&no=0'

    data = single_url_scraper(url)
    
    # Writeout

    with open(outfile, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=XPATH.keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

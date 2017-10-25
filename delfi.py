#!/usr/bin/python3


import csv
from lxml import html
import requests
import re


url = 'https://www.delfi.lt/verslas/verslas/apklause-apie-kainas-ir-algas-tokio-issiskyrimo-dar-nera-buve.d?id=76047145'

outfile = 'z.csv'

s = 2
reg = 0


### XPATHs


XPATH = {
    'IP' : './div[@class="comment-date"]/text()',
    'Date' : './div[@class="comment-date"]/text()',
    'Time' : './div[@class="comment-date"]/text()',
    'Name' : 'string(./div[@class="comment-author"])',
    'Comment' : './div/div[@class="comment-content-inner"]/text()'
    }


### Regexes


regex = {
    'IP' : re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
    'Date' : re.compile('\d{4}-\d{1,2}-\d{1,2}'),
    'Time' : re.compile('\d{2}:\d{2}')
}


### Substitutions


subs = {
    'Name' : '[\t\n]',
    'Comment' : '[\t\n]',
    }
    
    
### Main loop


url = url + '&com=1' + '&reg=' + str(reg) + '&s=' + str(s) + '&no=0'

pg = requests.get(url)

main_list = list()

while pg.status_code == 200:
    
    tree = html.fromstring(pg.content.decode('utf-8'))
    
    for comment in tree.xpath('//div[@data-post-id!=""]'):
        
        new_line = dict()
        
        for field in XPATH.keys():
            try:
                raw = comment.xpath(XPATH[field])[0]
                if field in regex.keys():
                    raw = regex[field].findall(raw)[0]
                if field in subs.keys():
                    raw = re.sub(subs[field], '', raw)
                new_line[field] = raw
            except:
                pass
                
        main_list.append(new_line)
        
    if tree.xpath('//a[@class="comments-pager-arrow-last"]/@href'):
        url = tree.xpath('//a[@class="comments-pager-arrow-last"]/@href')[0]
    else:
        break
    print(url)
    pg = requests.get(url)

## Writeout


with open(outfile, 'w') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=XPATH.keys())
    writer.writeheader()
    for row in main_list:
        writer.writerow(row)


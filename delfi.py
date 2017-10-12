#!/usr/bin/python3


import csv
from lxml import html
import requests
import re


url = 'https://www.delfi.lt/gyvenimas/anapus-tikroves/ka-galite-suzinoti-apie-vyra-is-jo-zodiako-zenklo.d?id=75912131&com=1&reg=0&no=0&s=2'

pg = requests.get(url)

outfile = 'z.csv'

### Regexes


IP_re = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
date_re = re.compile('\d{4}-\d{1,2}-\d{1,2}')
time_re = re.compile('\d{2}:\d{2}')


### Main loop

main_list = list()

if pg.status_code == 200:
    
    tree = html.fromstring(pg.content.decode('utf-8'))
    
    for comment in tree.xpath('//div[@data-post-id]'):
        
        new_line= {
            'IP' : IP_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0], 
            'Date' : date_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0],
            'Time' : time_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0],
            'Name' : re.sub('[\n\t]', '', comment.xpath('./div[@class="comment-author"]/a/text()')[0]),
            'Comment': re.sub('[\n\t]', '', comment.xpath('./div/div[@class="comment-content-inner"]/text()')[0])
            }
        
        main_list.append(new_line)
        

## Writeout


with open(outfile, 'w') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=new_line.keys())
    writer.writeheader()
    for row in main_list:
        writer.writerow(row)


#!/usr/bin/python3


import csv
from lxml import html
import requests
import re


url = 'https://www.delfi.lt/verslas/verslas/apklause-apie-kainas-ir-algas-tokio-issiskyrimo-dar-nera-buve.d?id=76047145'

outfile = 'z.csv'

s = 2
reg = 0


### Regexes

regexes = {
    'IP' : re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
    'Date' : re.compile('\d{4}-\d{1,2}-\d{1,2}'),
    'Time' : re.compile('\d{2}:\d{2}')
}

### Main loop


url = url + '&com=1' + '&reg=' + str(reg) + '&s=' + str(s) + '&no=0'


pg = requests.get(url)

main_list = list()

while pg.status_code == 200:
    
    tree = html.fromstring(pg.content.decode('utf-8'))
    
    for comment in tree.xpath('//div[@data-post-id!=""]'):
        
        new_line= {
            'IP' : IP_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0], 
            'Date' : date_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0],
            'Time' : time_re.findall(comment.xpath('./div[@class="comment-date"]/text()')[0])[0],
            'Name' : re.sub('[\n\t]', '', comment.xpath('./div[@class="comment-author"]/text()')[0]),
            'Comment': re.sub('[\n\t]', '', comment.xpath('./div/div[@class="comment-content-inner"]/text()')[0])
            }
        
        main_list.append(new_line)
        
    if tree.xpath('//a[@class="comments-pager-arrow-last"]/@href'):
        url = tree.xpath('//a[@class="comments-pager-arrow-last"]/@href')[0]
    else:
        break
    print(url)
    pg = requests.get(url)

## Writeout


with open(outfile, 'w') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=new_line.keys())
    writer.writeheader()
    for row in main_list:
        writer.writerow(row)


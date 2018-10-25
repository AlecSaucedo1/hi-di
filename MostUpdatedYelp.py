import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import urllib.request as ur
import json

endpoint = 'https://api.yelp.com/v3/businesses/search'
endpoint2 = 'https://api.yelp.com/v3/businesses/'
yp_id = 'uaGdzNm1BKEOqMewnreQANqQA3zfzFK6w1SFbSl2NvMUBRg0ZGsdn1cweOEJf-w_U1anl96Li5YMSKbyrFPLsYl7gOKnsIv6YVJ2rmCtf_rsY8SbU6uU5AhLR-VgW3Yx'
headers = {'Authorization': 'bearer ' + yp_id}
params = {'location': '94110', 'categories': 'bars', 'limit': '50'}

r = requests.get(endpoint, headers=headers, params=params)

r = json.loads(r.text)

y = 0
while y < len(r['businesses']) + 1:
    alias = r['businesses'][y]['alias']
    alias = alias.replace('ç', 'c').replace('è','e').replace('ñ','n').replace('ô','o').replace('ä','a').replace('é','e')
    y += 1
    x = 0
    while x < 4:
        if x == 0:
            ending = 'start=0'
            preUrl = 'https://www.yelp.com/biz/' + alias
            url = preUrl
            k = ur.urlopen(url)
            soup = BeautifulSoup(k, features="html.parser")
            text = soup.find_all(itemprop='description')
            text = str(text)
            text = text.replace('<p', '').replace('>', '').replace('<p itemprop="description"', '').replace('<p>',
                                                                                                            '').replace(
                '</p', '').replace('itemprop="description"', '')
            reviewSentiment1 = text
        elif x == 1:
            ending = 'start=20'
            preUrl = 'https://www.yelp.com/biz/' + alias + '?' + ending
            url = preUrl
            k = ur.urlopen(url)
            soup = BeautifulSoup(k, features="html.parser")
            text2 = soup.find_all(itemprop='description')
            text2 = str(text2)
            text2 = text2.replace('<p', '').replace('>', '').replace('<p itemprop="description"', '').replace('<p>',
                                                                                                              '').replace(
                '</p', '').replace('itemprop="description"', '')
            reviewSentiment2 = text2
        elif x == 2:
            ending = 'start=40'
            preUrl = 'https://www.yelp.com/biz/' + alias + '?' + ending
            url = preUrl
            k = ur.urlopen(url)
            soup = BeautifulSoup(k, features="html.parser")
            text3 = soup.find_all(itemprop='description')
            text3 = str(text3)
            text3 = text3.replace('<p', '').replace('>', '').replace('<p itemprop="description"', '').replace('<p>',
                                                                                                              '').replace(
                '</p', '').replace('itemprop="description"', '')
            reviewSentiment3 = text3
        elif x == 3:
            ending = 'start=60'
            preUrl = 'https://www.yelp.com/biz/' + alias + '?' + ending
            url = preUrl
            k = ur.urlopen(url)
            soup = BeautifulSoup(k, features="html.parser")
            text4 = soup.find_all(itemprop='description')
            text4 = str(text4)
            text4 = text4.replace('<p', '').replace('>', '').replace('<p itemprop="description"', '').replace('<p>',
                                                                                                              '').replace(
                '</p', '').replace('itemprop="description"', '')
            reviewSentiment4 = text4
        x += 1
    massReview = reviewSentiment1 + ' ' + reviewSentiment2 + ' ' + reviewSentiment3 + ' ' + reviewSentiment4
    massReview = TextBlob(massReview)
    counter = 0
    for s in massReview.sentences:
        if s.polarity > .5:
            counter +=1
    print(alias , ' ' , str(counter))
    #print(alias, ' ', massReview.sentiment)

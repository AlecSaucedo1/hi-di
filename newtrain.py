import json
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from unidecode import unidecode
import location

massTextDict = {}
train = []
massTextDictList = []


def createDict(masterAlias):
    reviewsCalled = {}
    for x in masterAlias:
        reviewsCalled[x] = masterAlias[0]
        everythingElse = masterAlias[1:]
        reviewsCalled[x] = everythingElse


def createAlias(alias, massText, zip, distance, massTextDict):
    counter = 0
    massText = TextBlob(massText)
    for i in massText.sentences:
        if i.polarity > massText.polarity:
            counter += 1
    masterAlias = [alias, massText.polarity, massText.subjectivity, counter, zip, distance, len(massText.sentences)]
    createDict(masterAlias)
    makeMassiveText(massTextDict, alias, massText)
    trainNaiveBayes(massTextDict, train)
    return masterAlias, massText


def makeMassiveText(massTextDict, alias, massText):
    massTextDict[alias] = massText
    massTextDictList.append(massTextDict)
    return massTextDict


def employBayes(cl, massTextDict):
    for k in massTextDict:
        prob_dist = cl.prob_classify(massTextDict[k])
        print(round(prob_dist.prob(1), 4))
        print(round(prob_dist.prob(-1), 4))
        print(k, cl.classify(massTextDict[k]))
       # print(cl.accuracy(massTextDict[k]))


def trainNaiveBayes(massTextDict, train):
    positiveCount = 0
    negativeCount = 0
    for k in massTextDict:
        trainLine = massTextDict[k]
        for i in trainLine.sentences:
            if i.polarity > 0.1 and i.subjectivity < .8:
                line = (i, 1)
                if line in train:
                    continue
                else:
                    if negativeCount >= positiveCount:
                        line = (str(i),1)
                        train.append(line)
                        positiveCount += 1
                    else:
                        continue
            elif i.polarity < 0.1 and i.subjectivity < .8:
                line = (i, -1)
                if line in train:
                    continue
                else:
                    if positiveCount >= negativeCount:
                        line = (str(i),-1)
                        train.append(line)
                        negativeCount += 1
                    else:
                        continue
    print(positiveCount)
    print(negativeCount)
    print(train)
    count = 0
    for i in train:
        if i[1] == 1:
            count += 1
    print(str(count), '<--count|length-->', str(len(train)))
    cl = NaiveBayesClassifier(train)
    print(cl.accuracy(train))
    print(cl.show_informative_features(5))
    employBayes(cl, massTextDict)


def getReviews(basePoint):
    headers = {'User-Agent': 'Chrome/60.0.3112.90'}
    f = requests.get(basePoint, headers=headers)
    soup = BeautifulSoup(f.text, features='html.parser')
    text = soup.find_all('p', lang='en')
    text = str(text)
    text = text.replace('\n', '').replace('<p', '').replace('</p>', '').replace('itemprop="description', '').replace(
        'lang="en"', '').replace('<br/', '').replace('<br>', '').replace('</br>', '')
    return text


def getMyLocation():   # if running mobile
    local = location.get_location()
    mylatitude = local['latitude']
    mylongitude = local['longitude']
    return mylatitude, mylongitude


def makeAPICall(category, mylatitude, mylongtitude, sort_by='', offset=''):
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    yp_id = 'uaGdzNm1BKEOqMewnreQANqQA3zfzFK6w1SFbSl2NvMUBRg0ZGsdn1cweOEJf-w_U1anl96Li5YMSKbyrFPLsYl7gOKnsIv6YVJ2rmCtf_rsY8SbU6uU5AhLR-VgW3Yx'
    headers = {'Authorization': 'bearer ' + yp_id}
    params = {'latitude': mylatitude, 'longitude': mylongtitude, 'categories': category, 'limit': '20',
              'sort_by': sort_by, 'offset': offset}
    r = requests.get(endpoint, headers=headers, params=params)
    r = json.loads(r.text)
    return r


def textMaker(endpoint2, alias, zip, distance):
    for x in range(4):
        if x == 0:
            basePoint = endpoint2 + alias
            text = getReviews(basePoint)
            x += 1
        elif x == 1:
            start = '?start=20'
            basePoint = endpoint2 + alias + start
            text2 = getReviews(basePoint)
            x += 1
        elif x == 2:
            start = '?start=40'
            basePoint = endpoint2 + alias + start
            text3 = getReviews(basePoint)
            x += 1
        elif x == 3:
            start = '?start=60'
            basePoint = endpoint2 + alias + start
            text3 = getReviews(basePoint)
            x += 1
            massText = text + text2 + text3
            createAlias(alias, massText, zip, distance, massTextDict)
    else:
        offset = 50
        return offset


def rateReviews(r):
    for k in r['businesses']:
        alias = k['alias']
        alias = unidecode(alias)
        zip = k['location']['zip_code']
        distance = k['distance']
        endpoint2 = 'https://www.yelp.com/biz/'
        textMaker(endpoint2, alias, zip, distance)

"""
mylatitude = getMyLocation()
mylatitude = str(mylatitude[0])
mylongitude = getMyLocation()
mylongitude = str(mylongitude[1])
"""

mylatitude = '37.787641'
mylongitude = '-122.437166'

# 37.760195, -122.421675 19th and Valencia
# 37.787641, -122.437166 Cali and Pine
# (37.7764642, -122.4415953)
# (37.7888580, -122.4200283)

offset = '0'
if offset == '0':
    offset = 0
    r = makeAPICall('bars', mylatitude, mylongitude, 'distance', offset)
    print(mylatitude, mylongitude)
    rateReviews(r)
    offset = '50'
else:
    offset = '50'
    r = makeAPICall('bars', mylatitude, mylongitude, 'distance', offset)
    rateReviews(r)

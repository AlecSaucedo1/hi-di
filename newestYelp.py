import json
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import urllib.request as ur
from unidecode import unidecode
import location

def createAlias(alias,massText):
  massText = TextBlob(massText)
  masterAlias = alias, massText.polarity, massText.subjectivity
  print(masterAlias)
  
def getReviews(basePoint):
  f = ur.urlopen(basePoint)
  soup = BeautifulSoup(f, 'html5lib')
  text = soup.find_all('p', lang='en')
  text = str(text)
  text = text.replace('\n', '').replace('<p', '').replace('</p>', '').replace('itemprop="description', '').replace('lang="en"', '').replace('<br/', '')
  return text

def getMyLocation():
  local = location.get_location()
  mylatitude = local['latitude']
  mylongitude = local['longitude']
  return mylatitude, mylongitude

def makeAPICall(category,mylatitude,mylongtitude,sort_by='',offset=''):
  endpoint = 'https://api.yelp.com/v3/businesses/search'
  yp_id = ##
  headers = {'Authorization': 'bearer ' + yp_id}
  params = {'latitude':mylatitude,'longitude':mylongtitude,'categories':category,'limit':'50','sort_by':sort_by,'offset':offset}
  r = requests.get(endpoint, headers=headers, params=params)
  r = json.loads(r.text)
  return r
  
def rateReviews(r,y=0):
  for k in r['businesses']:
      alias = k['alias']
      endpoint2 = 'https://www.yelp.com/biz/'
      x=0
      for x in range(3):
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
          massText = text + text2 + text3
          createAlias(alias,massText)

mylatitude = getMyLocation()
mylatitude = str(mylatitude[0])
mylongitude = getMyLocation()
mylongitude = str(mylongitude[1])
r = makeAPICall('bars',mylatitude,mylongitude,'distance',50)
rateReviews(r)

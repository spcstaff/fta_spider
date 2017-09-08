import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pprint
import time
import re

savePath = "/Users/lszlawrence/PycharmProjects/fta_spider/download"
homepage_URL = "https://www.transit.dot.gov/funding/grants/"
year = "fy-2015-statistical-summary"
file_path = []


def get_file_path():
    for i in range(2015, 2016, 1):
        year_summary = "fy-%s-statistical-summary" % i
        cur_url = homepage_URL + year_summary
        web_data = requests.get(cur_url)
        soup = BeautifulSoup(web_data.text, 'lxml')

        locations = soup.article.div.find_all("a", class_=False, href=re.compile("/funding/grants/"))
        #print(len(locations))
        for j in range(6, len(locations)):
            if j == 19:
                continue
            name = locations[j].get('href').split('/')[3]
            # pprint.pprint(name)
            link = "https://www.transit.dot.gov" + str(locations[j].get('href'))

            file_path.append((name, link))
    print(len(file_path))
    pprint.pprint(file_path)

links = []


def get_links():
    get_file_path()
    time.sleep(1)
    for link in file_path:
        web_data = requests.get(link[1])
        soup = BeautifulSoup(web_data.text, 'lxml')

        locations = soup.article.find_all("a", href=re.compile("https"))
        for location in locations:
            names = location.get('href').split('/')
            name = names[len(names) - 1]
            link1 = str(location.get('href'))
            print(link1)
            links.append((name, link1))
    pprint.pprint(links)

# get_links()


def get_contents(link):
    time.sleep(2)
    try:
        urllib.request.urlretrieve(link[1], "%s" % link[0])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_links()
    pool = Pool()
    pool.map(get_contents, links)
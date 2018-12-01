#!usr/bin/python3
#-*- coding:utf-8 -*-

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

URLS = 'https://www.552ze.com'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100'}


def requestLinks(URL, header):
    # nextPage = []
    addr = []
    nextLink, links = getNext(URL, header)
    # res = requests.get(URL, headers=header)
    # res.encoding='utf-8'
    # html = res.text
    # soup = BeautifulSoup(html,'html.parser')
    # links = soup.find(class_='box-topic-list p-0 clearfix')
    # nextLink = soup.find(class_='next pagegbk')
    while nextLink is not None:
        url = URLS + nextLink.get('href')
        # nextPage.append(url)
        for link in links:
            urlink = URLS + link.get('href')
            addr.append(urlink)
        nextLink, links = getNext(url, header)
    # print(nextPage)
    # print(addr)
    print('finished reading catalog......')
    print('starting reading content......')
    readAndWrite(addr)


def getNext(URL, header):
    res = requests.get(URL, headers=header, verify=False)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find(class_='box-topic-list p-0 clearfix')
    links = links.find_all('a')
    nextLink = soup.find(class_='next pagegbk')
    return nextLink, links


def readAndWrite(addr):
    DIRT = 'E:\\workspace\\dict_python\\readNovel\\Novel\\'
    count = 0
    for link in addr:
        res = requests.get(link, headers=header, verify=False)
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find(class_='text-overflow')
        title = title.string
        # print(title.string)
        text = soup.find(class_='layout-box clearfix')
        text = text.get_text("\n")
        # print(text)
        dirr = DIRT + str(count) + '.txt'
        print('writing the %d content...' % count)
        with open(dirr, 'w') as f:
            try:
                f.write(text)
            except Exception as e:
                print('exixts error...', e)
                continue
        count += 1
    print('Write a total of %d txt.....' % count)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    URL = URLS+'/html/news/45/'
    print('starting reading catalog......')
    requestLinks(URL, header)
    print('ending......')
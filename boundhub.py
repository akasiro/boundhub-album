# -*- coding: utf-8 -*-
import requests,re,os,time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scrapy_tool.scrapy_tool import *
class spider(object):
    def __init__(self):
        self.currentpath = os.getcwd()
        self.datapath = os.path.join(os.path.dirname(self.currentpath),'data')
        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)
        base_url = 'https://www.boundhub.com/'
        self.st = scrapy_tool(test_url= base_url,china=False)
        self.proxies = self.st.random_proxy()
        print('use proxies {}'.format(self.proxies))
        self.headers = self.st.random_headers()
    def startbymenberpage(self,menberpageurl):
        # 下载网页
        try:
            response = requests.get(menberpageurl,proxies = self.proxies, headers = self.headers, timeout = 5)

            pagesource = response.text
            # 解析网页，分析每个album的地址
            pattern = re.compile(r'https://www.boundhub.com/albums/\d+/[\w-]+/')
            albumurls = re.findall(pattern,pagesource)
            print(albumurls)
            # 处理每个album地址
            for albumurl in albumurls:
                self.enteralbum(albumurl)
        except:
            print('changing proxies')
            self.proxies = self.st.change_proxy()
            print('proxy change')
            self.startbymenberpage(menberpageurl)
        # nextpage
        #   判断是否有下一页
        # soup = BeautifulSoup(pagesource,'html.parser')
        # currentpageli = soup.find('li',{'class':'page-current'})
        # nextli = currentpageli.findNext('li')
        # if nextli['class'] != 'jump':
        #     nextpageurl = nextli.a['href']
        #     nextpageurl = urljoin(menberpageurl,nextpageurl)
        #     self.startbymenberpage(nextpageurl)



    def enteralbum(self,albumurl):
        try:
        #下载网页
            response = requests.get(albumurl, headers = self.headers, proxies = self.proxies,timeout = 5)
            #获得title和每个photo的链接
            pagesource = response.text
            soup = BeautifulSoup(pagesource,'html.parser')
            title = soup.find('div',{'class': 'headline'}).h2.get_text()
            albumpath = os.path.join(self.datapath,title)
            pattern = re.compile(r'https://www.boundhub.com/get_image/\d+/\w+/sources/[\d/]+.jpg/')
            photourls = re.findall(pattern,pagesource)
            #建立一个对应的文件夹
            if not os.path.exists(albumpath):
                os.mkdir(albumpath)
            #下载每个图片到文件加路径下
            for photourl in photourls:
                self.downloadphoto(photourl,albumpath)

            #报告下载成功，并休息
            print('success download {}'.format(title))
            time.sleep(20)
        except:
            print('changing proxies')
            self.proxies = self.st.change_proxy()
            print('proxy change')
            self.enteralbum(albumurl)



    def downloadphoto(self,purl,albumpath):
        pattern = re.compile(r'\d+.jpg')
        photoname = re.findall(pattern,purl)[0]

        photopath = os.path.join(albumpath,photoname)
        if not os.path.exists(photopath):
            try:
                r = requests.get(purl, headers = self.headers, proxies = self.proxies)
                with open(photopath,'ab+') as f:
                    f.write(r.content)
                time.sleep(10)
            except:
                print('changing proxies')
                self.proxies = self.st.change_proxy()
                print('proxy change')
                self.downloadphoto(purl,albumpath)




if __name__ == "__main__":
    menberurl = 'https://www.boundhub.com/members/67189/albums/'
    albumurl = 'https://www.boundhub.com/albums/7508/f00addcf2def889a6ad69a81fbdda728/'
    photourl = 'https://www.boundhub.com/get_image/2/8f7386c6ef5bb7bf017db1e768be6f55/sources/5000/5239/114007.jpg/'
    testspider = spider()
    #testspider.startbymenberpage(menberurl)
    testspider.enteralbum(albumurl)
    # testspider.downloadphoto(photourl,'Bondage outdoor exposure [English]1-4')




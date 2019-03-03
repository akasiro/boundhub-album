# -*- coding: utf-8 -*-
import requests,re,os,time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
class spider(object):
    def __init__(self):
        self.currentpath = os.getcwd()
        self.datapath = os.path.join(os.path.dirname(self.currentpath),'data')
        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)
    def startbymenberpage(self,menberpageurl):
        # 下载网页
        response = requests.get(menberpageurl)
        pagesource = response.text
        # 解析网页，分析每个album的地址
        pattern = re.compile(r'https://www.boundhub.com/albums/\d+/[\w-]+/')
        albumurls = re.findall(pattern,pagesource)
        print(albumurls)
        # 处理每个album地址
        for albumurl in albumurls:
            self.enteralbum(albumurl)

        # nextpage
        #   判断是否有下一页
        soup = BeautifulSoup(pagesource,'html.parser')
        currentpageli = soup.find('li',{'class':'page-current'})
        nextli = currentpageli.findNext('li')
        if nextli['class'] != 'jump':
            nextpageurl = nextli.a['href']
            nextpageurl = urljoin(menberpageurl,nextpageurl)
            self.startbymenberpage(nextpageurl)



    def enteralbum(self,albumurl):
        #下载网页
        response = requests.get(albumurl)
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
        time.sleep(60)



    def downloadphoto(self,purl,albumpath):
        pattern = re.compile(r'\d+.jpg')
        photoname = re.findall(pattern,purl)[0]

        photopath = os.path.join(albumpath,photoname)
        if not os.path.exists(photopath):
            r = requests.get(purl)
            with open(photopath,'ab+') as f:
                f.write(r.content)
            time.sleep(10)



if __name__ == "__main__":
    menberurl = 'https://www.boundhub.com/members/67189/albums/'
    albumurl = 'https://www.boundhub.com/albums/5239/bondage-outdoor-exposure-english-1-4/'
    photourl = 'https://www.boundhub.com/get_image/2/8f7386c6ef5bb7bf017db1e768be6f55/sources/5000/5239/114007.jpg/'
    testspider = spider()
    testspider.startbymenberpage(menberurl)
    #testspider.enteralbum(albumurl)
    #testspider.downloadphoto(photourl,'Bondage outdoor exposure [English]1-4')




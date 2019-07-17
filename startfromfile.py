#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os,re,time
from boundhub import *
from scrapy_tool.scrapy_tool import *


# In[2]:


st = scrapy_tool('https://www.boundhub.com/', china = False)


# In[3]:


def enteralbum2(filename,filepath = 'html'):
    url = os.path.join(filepath,filename)
    with open(url, 'r') as f:
        pagesource = f.read()
    title = filename.replace('.html','')
    print('start download {}'.format(title))
    albumpath = os.path.join("..","data",title)
    pattern = re.compile(r'https://www.boundhub.com/get_image/\d+/\w+/sources/[\d/]+.jpg/')
    photourls = re.findall(pattern,pagesource)
    #建立一个对应的文件夹
    if not os.path.exists(albumpath):
        os.mkdir(albumpath)
    #print(photourls)
    #下载每个图片到文件加路径下
    for i in range(len(photourls)):
        downloadphoto2(photourls[i],albumpath)
        print('-|{}| {:.2f}%'.format(('#'*int((i+1)/len(photourls)*100)).ljust(100,'-'),(i+1)/len(photourls)*100))
        print('\r')
    
    #报告下载成功，并休息
    print('\nsuccess download {}'.format(title))
    time.sleep(1)
def downloadphoto2(purl, albumpath):
    pattern = re.compile(r'\d+.jpg')
    photoname = re.findall(pattern,purl)[0]

    photopath = os.path.join(albumpath,photoname)
    if not os.path.exists(photopath):
        r = st.requests_st(purl)
        with open(photopath, 'ab+') as f:
            f.write(r.content)
        #print(purl)
        time.sleep(1)

def download_by_htmls(filepath = 'html'):
    for i in os.listdir(filepath):
        enteralbum2(i,filepath = filepath)


# In[ ]:

if __name__ == '__main__':
    download_by_htmls()


# In[ ]:





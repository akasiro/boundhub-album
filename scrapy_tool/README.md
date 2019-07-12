# Scrapy tool


这是能够为爬虫提供IP和headers的小程序



**环境：Python3**


## 依赖的库
requests, bs4
```
pip3 install requests, bs4
```

## 使用说明
1. 安装：将项目clone到python爬虫的项目中
```
git clone https://github.com/akasiro/scrapy_tool.git
```

2. 导入：再python爬虫中导入项目
```
from scrapy_tool.scrapy_tool import *
```

3. 获取随机的ip和headers
```
st = scrapy_tool()
random_proxies = st.random_proxy()
random_headers = st.random_headers()
response = requests.get(url, headers = random_headers, proxies = random_proxies)
```

##拓展说明
本程序在获取代理ip过程中还可以配合qiyeboy/IPProxyPool使用
可以提前安装并运行七夜的IPProxyPool，本程序将会使用IPProxyPool获取的ip池中的ip
```
git clone https://github.com/qiyeboy/IPProxyPool.git
cd IPProxyPool
python IPProxy.py
```
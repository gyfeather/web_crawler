#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/6/6 21:10
#!@Author ： gyfeather
#!@File :.py

from selenium import webdriver
import re
from random import choice
import requests
import bs4
import random
def get_proxy_ip_port():   #获取浏览器代理

    url = "http://www.xicidaili.com/"

    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
    "Accept-Encoding":"gzip",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Referer":"http://www.xicidaili.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
    }
    # r = requests.get(url)

    r = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(r.text,"lxml")
    data = soup.table.find_all("td",limit=40)    # limit是获取td的个数，这里可以指定获取多少个IP
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
    port_compile = re.compile(r'<td>(\d+)</td>')
    ip = re.findall(ip_compile,str(data))
    port = re.findall(port_compile,str(data))
    ips = [":".join(i) for i in zip(ip,port)]

    print(len(ips))
    a=random.randint(0,len(ips)-1)   #取代理池长度
     #随机生成1-5的整数
    # print ips[a].split(":")
    b=ips[a].split(":")
    print type(b[0]),b[0]
    print type(b[1]),b[1]
    return b
    # return ips   #伪代理用

if __name__ == '__main__':

    get_proxy_ip_port()
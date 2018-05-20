#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/5/20 20:40
#!@Author ： gyfeather
#!@File :.py
#webdriver的CSS选择器可以很好的定位，但是遇到网页变化则易产生错误，因此此次爬虫选择正则匹配的方式

from selenium import webdriver
import re
import requests
from bs4 import BeautifulSoup
import lxml
from sqlalchemy.sql import func
import sys,os
#初始化存档路径，及浏览器设置（无头模式）

download_path = u'C:/Users/gyfea/Desktop'
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
key_word_outer = re.compile(ur'^/zhengwugongkai/127924/128041/2951606/1923625/1923629/*')

def get_profile():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir',download_path)
    profile.set_preference('browser.download.folderList',2)
    profile.set_preference('browser.download.manager.showWhenStarting', True)
    profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                           "application/zip,text/plain,application/vnd.ms-excel,application/vnd.ms-word,text/csv,\
                           text/comma-separated-values,\
                           application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,\
                           application/vnd.openxmlformats-officedocument.wordprocessingml.document,\
                           application/msword,application/msexcel,\
                           application/octet-stream,\
                           application/x-xls,application/pdf,\
                           image/tiff,image/jpeg")
    return profile

# brower.get("'http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/index.html")
def generate_branch_list():
    headers = {
        'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'wzwsconfirm=6a3e166584aa56c18cc70b99d10e0999; wzwstemplate=Ng==; wzwschallenge=-1; ccpassport=01e0a29d398f84b71fa3ec5c3900ad6b; wzwsvtime=1526820666',
        'Host': 'www.pbc.gov.cn',
        'Referer': "http://www.pbc.gov.cn/zhengwug…606/1923625/1923629/index.html",
        'Upgrade-Insecure-Requests': '1',
        "user-agent":"Mozilla / 5.0(Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    rmyh=r'http://www.pbc.gov.cn'
    url=r'http://www.pbc.gov.cn/zhengwugongkai/127924/128041/2951606/1923625/1923629/index.html'#行政审批网页
    html=get_js_html(url)
    print "hello world"
    # r= requests.get(html,headers=headers)
    soup = BeautifulSoup(html,"lxml")
    public_xml = soup.find_all('a',href=key_word_outer)#正则匹配许可超链接
    cwd=os.getcwd()
    print cwd
    with open(cwd+r'/branch_list.txt','w+') as fout:

        for link in public_xml[2:]:     #打印每一个链接
            fout.write(link.get('href'))
            fout.write('\n')
        # print link.get('href')


    # branch_table = soup[63]
    # atags = branch_table.find_all('a')

def get_js_html(url):
    profile = get_profile()
    brower = webdriver.Firefox(firefox_profile=profile, firefox_options=fireFoxOptions)
    r= brower.get(url)
    return brower.page_source.encode('utf-8')

def download_js(url,href_text,content_type = None):
    brower.get(url)
    button = brower.find_element_by_link_text(href_text)
    prev_files_length = len(os.listdir(download_path))
    button.click()
    try_count = 0
    while True:
        time.sleep(try_sleep_interval)
        after_files_length = len(os.listdir(download_path))
        if after_files_length > prev_files_length:
            break
        try_count += 1
        if try_count >= try_timeout_count:
            break

if __name__ == '__main__':
    generate_branch_list()
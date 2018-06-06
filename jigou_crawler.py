#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/5/20 20:40
#!@Author ： gyfeather
#!@File :.py
#webdriver的CSS选择器可以很好的定位，但是遇到网页变化则易产生错误，因此此次爬虫选择正则匹配的方式

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import lxml
from sqlalchemy.sql import func
import sys,os
import numpy as np
from time import sleep, ctime


#初始化存档路径，及浏览器设置（无头模式）
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
binary=FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
download_path = u'C:/Users/gyfea/Desktop'

key_word_outer = re.compile(ur'^/zhengwugongkai/127924/128041/2951606/1923625/1923629/*') #匹配处罚链接
key_word_page = re.compile(ur'^分*页$')  #匹配页数
key_word_page1 = re.compile(ur'分13页')  #匹配页数
key_word = re.compile(u'^机构详细信息')

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
    html = get_js_html(url)
    soup = BeautifulSoup(html,"lxml")



    #查找行政许可总页数，没找到id,只能通过tagname和属性来查找
    total_page0=soup.find_all('td',attrs={"class":"Normal","valign":"bottom","nowrap":"true","align":"center"})
    for i in total_page0:
        total_page1=i.get_text().split()[1]  #获取的文字很多，用字符串分割后，取第二个。
        total_page=filter(str.isdigit,total_page1.encode('gbk'))   #从数字和字符串里面，取数字，用到filter，并注意转码

    print "总共有"+total_page+"页"

    #取当前页链接并写入txt
# def get_current_page():
    public_xml = soup.find_all('a',href=key_word_outer)#正则匹配许可超链接
    source_address=r'D:/code/web_crawler/branch_list.txt'
    with open(source_address,'a') as fout:
        for link in public_xml[2:]:     #将每一个链接，补全完整路径并写入TXT文档，
            fout.write(rmyh+link.get('href'))
            fout.write('\n')



    #取下一页,并读入soup
    for i in range(1,int(total_page),1):
        next_page_tag = rmyh + soup.find('a', text='下一页').get('tagname')
        print next_page_tag
        html=  get_js_html(next_page_tag)
        soup = BeautifulSoup(html, "lxml")
        public_xml = soup.find_all('a',href=key_word_outer)#正则匹配许可超链接
        source_address=r'D:/code/web_crawler/branch_list.txt'
        with open(source_address,'a') as fout:
            for link in public_xml[2:]:     #将每一个链接，补全完整路径并写入TXT文档，
                fout.write(rmyh+link.get('href'))
                fout.write('\n')


def get_js_html(url):
    profile = get_profile()
    brower = webdriver.Firefox(firefox_profile=profile, firefox_options=fireFoxOptions,firefox_binary=binary)
    r= brower.get(url)
    return brower.page_source.encode('utf-8')

def download_branch_information():   #下载机构信息
    #初始化表头信息
    caption = ["许可证编号", "公司名称", "法定代表人（负责人）", "住所（营业场所）", "业务类型", "业务覆盖范围", "换证日期", "首次许可日期", "有效期至", "备注"]
    caption1 = np.array(caption).reshape((1, 10))
    start_caption = pd.DataFrame(caption1)
    start_caption.to_csv("C:/Users/gyfea/Desktop/branch_information.csv", mode="a", encoding="utf_8_sig", index=0,
                         header=0)

    #读取分支机构信息，先数组化再字符化，
    data = pd.read_table(r'D:/code/web_crawler/branch_list.txt', header=None, encoding='gb2312')
    link_all=np.array(data).tolist()
    id1=0

    #循环读入地址，并抓取信息
    try:
        while id1<len(link_all):
            where = "".join(link_all[id1])  # 读取数组变字符串
            print where
            id1=id1+1



            #打开字符串化后的网页，爬取数据
            html = get_js_html(where)
            soup = BeautifulSoup(html, "lxml").find(text=key_word)  # 关键字并找父标签
            # # soup = BeautifulSoup(html, "lxml").select("table")[15].find("td").get_text() #解析网页后找到第15个表格的所有文字
            # list=soup.strip().replace(' ', '').split('\n')  #对文字进行处理，并按换行符分割成数组
            soup1=soup.parent.parent.parent.parent.parent.get_text()# 解析网页后找到父标签的所有文字
            list = soup1.strip().replace(' ', '').split('\n') # 对文字进行处理，并按换行符分割成数组
            list1=list[4::4]
            # for i in range(4, len(list), 4):
            #     list1.append(list[i])

            #表格信息不规范，标准的10行，有的只有9行，甚至8行，都需要补足

            print len(list1)
            if len(list1)==9:
                list1.append("None")
            if len(list1)==8:
                list1.insert(6,"None") #没有换证日期，加上字符串
                list1.append("None")  #没有备注，加上字符串


            #结果写入CSV
            result11 = np.array(list1).reshape((1, 10))
            final_result = pd.DataFrame(result11)
            final_result.to_csv("C:/Users/gyfea/Desktop/branch_information.csv", mode="a", encoding="utf_8_sig", index=0,
                                header=0)
            print list1[0]
            sleep(2)
            soup=None
    #出现异常后，休息两秒重新加载执行
    except:
        print "出现异常，此机构未成功！"
        sleep(2)

    finally:
            print "finished!"

if __name__ == '__main__':
    # generate_branch_list()
    download_branch_information()
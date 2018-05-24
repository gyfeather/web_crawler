#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/5/23 21:43
#!@Author ： gyfeather
#!@File :.py

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep, ctime
import sys,os
import xlwt
import pandas as pd
import numpy as np
import requests
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
key_word1 = re.compile(u'^ICP备案主体信息')
key_word2 = re.compile(u'^ICP备案网站信息')


#初始化存档路径，及浏览器设置（无头模式）
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

# binary=FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
download_path = u'C:/Users/gyfea/Desktop'

def get_js_html(url):
    profile = get_profile()
    brower = webdriver.Firefox(firefox_profile=profile, firefox_options=fireFoxOptions)
    r= brower.get(url)
    return brower.page_source.encode('utf-8')

def get_profile():
    profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.download.dir',download_path)
    # profile.set_preference('browser.download.folderList',2)
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

driver = webdriver.Firefox()
driver.get(r"http://www.beianbeian.com/")
# html=get_js_html(r"http://www.beianbeian.com/")
# soup = BeautifulSoup(html,"lxml")

# Select(self.driver.find_element_by_id("select")).
driver.find_element_by_css_selector('.info3 > select:nth-child(1)').find_elements_by_tag_name("option")[2].click()
# driver.find_element_by_tag_name("option")[2]

# s1.select
driver.find_element_by_css_selector(".input").send_keys(u"九派天下支付有限公司")
sleep(2)
driver.find_element_by_css_selector(".but").click()
driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td[4]/a[1]").click()
# s2=driver.find_element_by_xpath("/html/body/div/div[6]/a").text
# s1="超链目标指向".decode("utf-8","ignore")
sleep(5)
handles=driver.window_handles
print handles
driver.switch_to_window(handles[1])

url = driver.find_element_by_css_selector(".wrap > div:nth-child(9) > a:nth-child(2)").get_attribute("href")
html = get_js_html(url)
soup_main = BeautifulSoup(html, "lxml").find(text=key_word1)#查找ICP主体备案信息
soup_net= BeautifulSoup(html, "lxml").find(text=key_word2)#查找ICP网站备案信息
soup1 = soup_main.parent.parent.parent.get_text()
soup2 = soup_net.parent.parent.parent.get_text()
#
list1 = soup1.strip().replace('\n\n','').split('\n')[2:9:2]# 对文字进行处理，并按两个换行符的表格替代为空换行符分割成数组
# print len(list1)
list2 = soup2.strip().replace("\n\n\n","").replace('\n\n','').split('\n')[3:8:2]# 对文字进行处理，并按两个换行符的表格替代为空换行符分割成数组
# list2 = listx
list3 = list1+list2
print len(list3)
print "hello world"
# list3=list1+list2
result11 = np.array(list3).reshape((1,7))
final_result = pd.DataFrame(result11)
final_result.to_csv("C:/Users/gyfea/Desktop/ICP_information.csv", mode="a", encoding="utf_8_sig", index=0, header=0)

# if __name__ == '__main__':

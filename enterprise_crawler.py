# # -*- coding:utf-8 -*-
# #@Time :2018/5/15 22:44
# #!@Author ： gyfeather
# #!@File :.py
#  CSS下#代表id,  .代表class
#多种定位法，id,name,tagname,xpath(绝对路径和相对路径),css(相对路径)
#注意嵌套的iframe，需要swith_to_frame

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep, ctime
import sys,os
import pandas as pd
import numpy as np
import random
from proxy import get_proxy_ip_port
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
# 据说selenium不用修改headers
# headers = {
#         'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate',
#         "user-agent":"Mozilla / 5.0(Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0"
#     }

def start_excel():  #初始化目标excel

    caption = ["公司名称", "注册资本", "实缴资本", "经营状态", "成立日期", "统一社会信用代码", "纳税人识别号", "注册号", "组织机构代码", "公司类型", "所属行业", "核准日期",
               "登记机关", "所属地区", "英文名", "曾用名", "经营方式", "人员规模", "营业期限", "企业地址", "经营范围"]
    caption1=np.array(caption).reshape((1,21))
    start_caption = pd.DataFrame(caption1)
    start_caption.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv", mode="a",encoding="utf_8_sig",index=0,header=0)
    #header=0不保留列名,index=0不需要行索引
    #读取搜索的企业名称
    global enterprise_names
    enterprise_name1= pd.read_csv("C:/Users/gyfea/Desktop/enterprise_list.csv",header=0) #获取第一列数据

    enterprise_names= np.array(enterprise_name1).tolist()  #变成序列，再变成数组tolist



def open_web():
    enterprise_names = np.array(pd.read_csv("C:/Users/gyfea/Desktop/enterprise_list.csv", header=0)).tolist()   # 获取第一列数据
    # for enterprise_name in enterprise_names:
    #     print enterprise_name
    # os.system('pause')

    try:
        #主页填上搜索对象并提交
        b=0
        for enterprise_name in enterprise_names:
            driver = webdriver.Firefox()
            driver.get("http://www.qichacha.com/")
             # 隐藏等待最多5秒
            driver.implicitly_wait(5)
            # print enterprise_names
            qq1 = enterprise_name[0].decode('cp936')
            # str = qq1.encode('raw_unicode_escape')

            print "正在下载的企业是：", qq1  # 打印正在下载的企业信息名


            driver.find_element_by_css_selector("#searchkey").send_keys(u"%s"%qq1)
            driver.find_element_by_css_selector("#V3_Search_bt").click()
            result1 = []#结果初始化，并定点取值
            try:
                driver.find_element_by_class_name("ma_h1").click()
                #因为打开新窗口，因此需要获取并切换窗口句柄
                sleep(2)
                handles = driver.window_handles
                driver.switch_to_window(handles[-1])
                enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
                result1.append(enterprise_name)  #result1为结果集

                for i in range(1,12,1):
                    if i>=10:
                        aa = 'table.ntable:nth-child(4) > tbody:nth-child(1) > tr:nth-child(%s) > td:nth-child(2)' % (i)
                        bb = driver.find_element_by_css_selector(aa).text
                        result1.append(bb)
                    else:
                        for j in range(2, 6, 2):
                            aa = 'table.ntable:nth-child(4) > tbody:nth-child(1) > tr:nth-child(%s) > td:nth-child(%s)' % (i, j)
                            bb = driver.find_element_by_css_selector(aa).text
                            result1.append(bb)

                #如果找齐了字段就写入表格
                if len(result1)==21:
                    result11=np.array(result1).reshape((1,21))
                    final_result=pd.DataFrame(result11)
                    final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv",mode="a",encoding="utf-8",index=0,header=0)

            except:
                result1.append(qq1)
                result11 = np.array(result1)
                final_result = pd.DataFrame(result11)
                final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv", mode="a", encoding="utf-8", index=0, header=0)

            driver.quit()
            b=b+1   #计数
            print "已经爬取了:"+str(b)+"家企业"
    #报错信息
    except NoSuchElementException as msg:
        print msg

def open_web_agent():
    agent1 = get_proxy_ip_port() #生成代理IP池
    a = random.randint(0, len(agent1) - 1)    #随机选择ip
    try:
        #主页填上搜索对象并提交
        b=0
        for enterprise_name in enterprise_names:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http',agent1[0])
            profile.set_preference('network.proxy.http_port', int(agent1[1]))  # int
            profile.set_preference('network.proxy.ssl',agent1[0])
            profile.set_preference('network.proxy.ssl_port',int(agent1[1]))# int
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile=profile)

            driver.get("http://www.qichacha.com/")
            driver.implicitly_wait(5)   # 隐藏等待最多5秒
            qq1 = enterprise_name[0].decode('cp936')
            print "正在下载的企业是：", qq1  # 打印正在下载的企业信息名

            driver.find_element_by_css_selector("#searchkey").send_keys(u"%s"%qq1)
            driver.find_element_by_css_selector("#V3_Search_bt").click()
            result1 = []    #结果初始化，并定点取值
            try:
                driver.find_element_by_class_name("ma_h1").click()

                sleep(2)   #因为打开新窗口，因此需要等待获取并切换窗口句柄
                handles = driver.window_handles

                driver.switch_to_window(handles[-1])
                enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
                result1.append(enterprise_name)  #result1为结果集
                #分析目标数据地址后循环取数
                for i in range(1,12,1):
                    if i>=10:
                        aa = 'table.ntable:nth-child(4) > tbody:nth-child(1) > tr:nth-child(%s) > td:nth-child(2)' % (i)
                        bb = driver.find_element_by_css_selector(aa).text
                        result1.append(bb)
                    else:
                        for j in range(2, 6, 2):
                            aa = 'table.ntable:nth-child(4) > tbody:nth-child(1) > tr:nth-child(%s) > td:nth-child(%s)' % (i, j)
                            bb = driver.find_element_by_css_selector(aa).text
                            result1.append(bb)


                #如果找齐了字段就写入表格
                if len(result1)==21:
                    result11=np.array(result1).reshape((1,21))
                    final_result=pd.DataFrame(result11)
                    final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv",mode="a",encoding="utf-8",index=0,header=0)

            except:
                result1.append(qq1)
                result11 = np.array(result1)
                final_result = pd.DataFrame(result11)
                final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv", mode="a", encoding="utf-8", index=0, header=0)

            driver.quit()
            b=b+1   #计数
            print "已经爬取了:"+str(b)+"家企业"
    #报错信息
    except NoSuchElementException as msg:
        print msg




def get_csv_row(filename):  #获取指定文件的行数
    with open(filename) as file:
        print(len(file.readlines()))
        return len(file.readlines())

def information_hint():
    b = "Boss!企业信息正在下载，请稍等！"
    print b.decode("utf-8")
    import ctypes

if __name__ == '__main__':

    information_hint() #信息提示
    # start_excel()     #初始化目标excel文件
    # open_web_agent()        #使用代理爬取网页
    open_web()   #不使用代理爬取网页

    ctypes.windll.user32.MessageBoxA(0,u"恭喜老板！你要的企业工商信息已经批量下载完毕!".encode('gb2312'),u' 信息'.encode('gb2312'),0)



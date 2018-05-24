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
import xlwt
import pandas as pd
import numpy as np

from proxy import get_proxy_ip_port

from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType


def start_excel():
    #初始化列名
    caption = ["公司名称", "注册资本", "实缴资本", "经营状态", "成立日期", "统一社会信用代码", "纳税人识别号", "注册号", "组织机构代码", "公司类型", "所属行业", "核准日期",
               "登记机关", "所属地区", "英文名", "曾用名", "经营方式", "人员规模", "营业期限", "企业地址", "经营范围"]
    caption1=np.array(caption).reshape((1,21))
    start_caption = pd.DataFrame(caption1)
    start_caption.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv", mode="a",encoding="utf_8_sig",index=0,header=0)
    #header=0不保留列名,index=0不需要行索引
    #读取搜索的企业名称
    global enterprise_names
    enterprise_name1= pd.read_csv("C:/Users/gyfea/Desktop/enterprise_list.csv",header=0) #获取第一列数据
    # print type(enterprise_name1)
    enterprise_names= np.array(enterprise_name1).tolist()  #变成序列，再变成数组tolist

    # print type(enterprise_names)
    # print len(enterprise_names)
    # print enterprise_names
    # os.system("pause")


def open_web():


    # if sys.getdefaultencoding() != 'utf-8':
    #     reload(sys)
    #     sys.setdefaultencoding('utf-8')
    try:
        #主页填上搜索对象,并提交
        b=0   #计数用
        for enterprise_name in enterprise_names:

            proxy = Proxy(
                {
                    # 'proxyType': ProxyType.MANUAL,  # 用不用都行
                    'httpProxy': get_proxy_ip_port()
                }
            )
            print "现在使用的代理IP地址是："+ get_proxy_ip_port()
            driver = webdriver.Firefox(proxy=proxy)
            driver.get("http://www.qichacha.com/")

            # 隐藏等待最多5秒
            driver.implicitly_wait(5)
            # print enterprise_names
            qq1 = enterprise_name[0].decode('cp936')


            # # print type(qq1)
            # # print qq1.
            # os.system("pause")

            driver.find_element_by_css_selector("#searchkey").send_keys(u"%s"%qq1)
            driver.find_element_by_css_selector("#V3_Search_bt").click()
            result1 = []#结果初始化，并定点取值
            try:
                driver.find_element_by_class_name("ma_h1").click()

                # sleep(5)
                #因为打开新窗口，因此需要获取并切换窗口句柄
                sleep(2)
                handles = driver.window_handles
                # print(len(handles))
                # print(handles)
                driver.switch_to_window(handles[-1])




                # driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)") :
                enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
            #     enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
                result1.append(enterprise_name)  #result1为结果集
                sleep(2)
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
                    final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv",mode="a",encoding="utf_8_sig",index=0,header=0)

            except:
                result1.append(qq1)
                result11 = np.array(result1)
                final_result = pd.DataFrame(result11)
                final_result.to_csv("C:/Users/gyfea/Desktop/enterprise_information.csv", mode="a", encoding="utf_8_sig", index=0, header=0)

            driver.quit()
            b=b+1   #计数
            print "已经爬取了:"+str(b)+"家企业"
    #报错信息
    except NoSuchElementException as msg:
        print msg
    finally:
        print ctime()
if __name__ == '__main__':
    b= "Boss!企业信息正在下载，请稍等！"
    print b.decode("utf-8")
    import ctypes
    start_excel()
    open_web()
    print sys.getdefaultencoding()
    ctypes.windll.user32.MessageBoxA(0,u"恭喜老板！你要的企业工商信息已经批量下载完毕!".encode('gb2312'),u' 信息'.encode('gb2312'),0)



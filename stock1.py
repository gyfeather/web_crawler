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
def start_excel():
    caption = ["公司名称", "注册资本", "实缴资本", "经营状态", "成立日期", "统一社会信用代码", "纳税人识别号", "注册号", "组织机构代码", "公司类型", "所属行业", "核准日期",
               "登记机关", "所属地区", "英文名", "曾用名", "经营方式", "人员规模", "营业期限", "企业地址", "经营范围"]
    caption1=np.array(caption).reshape((1,21))
    start_caption = pd.DataFrame(caption1)
    start_caption.to_csv("D:/code/13548777325.csv", mode="a",encoding="utf_8_sig",index=0,header=0)#header=0不保留列名,index=0不需要行索引
   #循环写入xls
    # global sheet1,f
    # # f = xlwt.Workbook(encoding='utf-8')
    # sheet1= f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    # for index0 in range(len(result0)):  # 将表头写入EXCEL
    #     sheet1.write(0, index0, result0[index0])
    # f.save("13548777325.xls")
def open_web():
    import xlwt
    driver=webdriver.Firefox()
    driver.get("http://www.qichacha.com/")
    # driver.get("https://www.qichacha.com/firm_4e7da5447561e95925fd9a86178846c1.html")
    #隐藏等待最多5秒
    driver.implicitly_wait(5)
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    try:
        print ctime()#打印当前时间用于计时
        #主页填上搜索对象,并提交
        # enterprise_list=pd.read_excel("xxx")
        # np.array(pandas)
        driver.find_element_by_css_selector("#searchkey").send_keys(u"大连软银安通信息技术有限公司")
        driver.find_element_by_css_selector("#V3_Search_bt").click()
        driver.find_element_by_class_name("ma_h1").click()
    # sleep(5)
    #因为打开新窗口，因此需要获取并切换窗口句柄
        sleep(2)
        handles = driver.window_handles
        print(len(handles))
        print(handles)
        driver.switch_to_window(handles[-1])
    #结果初始化，并定点取值
        result1=[]
        enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
        result1.append(enterprise_name)
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


        # pd.read_excel("D:/code/13548777325.xls",sheet_name=None)
        if len(result1)==21:
            result11=np.array(result1).reshape((1,21))
            final_result=pd.DataFrame(result11)
            final_result.to_csv("D:/code/13548777325.csv",mode="a",encoding="utf_8_sig",index=0,header=0)
            # for  index1 in range(len(result1)):  #将内容写入EXCEL,从第二行起
            #     sheet1.write(1,index1,result1[index1])
            # f.save("13548777325.xls")


    #报错信息
    except NoSuchElementException as msg:
        print msg
    finally:
        print ctime()
if __name__ == '__main__':

    start_excel()
    open_web()







#2.登录QQ邮箱

# from selenium.webdriver.common.keys import Keys#
# import os
# import requests
# import lxml
# from bs4 import BeautifulSoup
# import xlwt
# # driver = webdriver.Firefox()
# # driver.get("https://mail.qq.com/cgi-bin/loginpage")
# # print driver.find_elements_by_id("u")
# #
# # time.sleep(100)
# # #用户名 密码
# #
# # # //*[@id="u"]
# #
# # driver.switch_to.frame("login_frame")
# # driver.find_element_by_id("switcher_plogin").click()
# #
# # driver.find_element_by_xpath("//*[@id='u']").send_keys("1041107644")
# # driver.find_element_by_xpath("//*[@id='p']").send_keys("gy0824ZY0606")
# # driver.find_element_by_xpath("//*[@id='login_button']").click()
# # # elem_pwd.find_element_by_id("login_button").click()
# # time.sleep(5)
#
# headers={"Accept":"*/*",
# "Accept-Encoding":"gzip, deflate",
# "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
# "Connection":"keep-alive",
# "Cookie":"UM_distinctid=16338636146449-0…c63fb5147f119f1075=1526544823",
# "Host":"tongji.qichacha.com",
# "Referer":"http://www.qichacha.com/",
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0"}
# driver = webdriver.Firefox()
# driver.get("http://www.qichacha.com/")
#
# driver.find_element_by_id("searchkey").send_keys(u"大连软银安通信息技术有限公司")
#
# driver.find_element_by_id("V3_Search_bt").click()
#
# # print driver.current_window_handle
# # driver.switchTo().window(handles1)
# # print driver.find_element_by_class_name("ma_h1")
# # print driver.find_element_by_class_name("ma_h1").id
# # print driver.find_element_by_class_name("ma_h1").tag_name
# driver.find_element_by_class_name("ma_h1").click()
# # driver.find_element_by_xpath(ur"/html/body/div[3]/div/div[1]/div[2]/section[2]/table[2]/tbody/tr[1]/td[1]")
# table1=driver.find_element_by_class_name(ur"table")
# rows = table1.find_element_by_tag_name("tr")
# print rows
# table_tr_list = driver.find_element(*table_loc).find_elements(By.TAG_NAME, "tr")
# driver.find_elements()
#
# # response = requests.get(url_now,headers = headers)
# # if response.status_code != 200:
# #         response.encoding = 'utf-8'
# #         print(response.status_code)
# #         print('ERROR')
# # soup = BeautifulSoup(response.text, 'lxml')
# # # print(soup)
# #
# # com_names = soup.find_all(class_='ma_h1')  # 获取公司名称
# # print com_names.
# # os.system("pause")
# # print(com_names)
# # com_name1 = com_names[1].get_text()
# # # print(com_name1)
# # peo_names = soup.find_all(class_='a-blue')  # 公司法人
# # # print(peo_names)
# # peo_phones = soup.find_all(class_='m-t-xs')  # 公司号码
# # # tags = peo_phones[4].find(text = True).strip()
# # # print(tags)
# # # tttt = peo_phones[0].contents[5].get_text()
# # # print (tttt)
# # else_comtent = peo_phones[0].find(class_='m-l')
# # print(else_comtent)
# # peo_emails=soup.find_all(class_='m-1')
# # global com_name_list
# # global peo_name_list
# # global peo_phone_list
# # global com_place_list
# # global zhuceziben_list
# # global chenglishijian_list
# # global email_list
# # print('开始爬取数据，请勿打开excel')
# # for i in range(0, len(com_names)):
# #     n = 1 + 3 * i
# #     m = i + 2 * (i + 1)
# #     try:
# #         peo_phone = peo_phones[n].find(text=True).strip()
# #         com_place = peo_phones[m].find(text=True).strip()
# #         zhuceziben = peo_phones[3 * i].find(class_='m-l').get_text()
# #         chenglishijian = peo_phones[3 * i].contents[5].get_text()
# #         email = peo_phones[n].contents[1].get_text()
# #
# #         # print('email',email)
# #         peo_phone_list.append(peo_phone)
# #         com_place_list.append(com_place)
# #         zhuceziben_list.append(zhuceziben)
# #         chenglishijian_list.append(chenglishijian)
# #         email_list.append(email)
# #     except Exception:
# #         print('exception')
# #
# # for com_name, peo_name in zip(com_names, peo_names):
# #     com_name = com_name.get_text()
# #     peo_name = peo_name.get_text()
# #     com_name_list.append(com_name)
# #     peo_name_list.append(peo_name)
# #
# # if __name__ == '__main__':
# #     com_name_list = []
# #     peo_name_list = []
# #     peo_phone_list = []
# #     com_place_list = []
# #     zhuceziben_list = []
# #     chenglishijian_list = []
# #     email_list = []
# #
# #     key_word = input('请输入您想搜索的关键词：')
# #     key_word.encode("utf-8")
# #     print('正在搜索，请稍后')
# #     for x in range(400, 500):
# #         if x == 1:
# #             url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word, x)
# #         else:
# #             url = r'http://www.qichacha.com/search_index?key={}&ajaxflag=1&p={}&'.format(key_word, x)
# #         # url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word,x)
# #         s1 = craw(url, key_word.encode("utf-8").decode("latin1"))
# #     workbook = xlwt.Workbook()
# #     # 创建sheet对象，新建sheet
# #     sheet1 = workbook.add_sheet('xlwt', cell_overwrite_ok=True)
# #     # ---设置excel样式---
# #     # 初始化样式
# #     style = xlwt.XFStyle()
# #     # 创建字体样式
# #     font = xlwt.Font()
# #     font.name = 'Times New Roman'
# #     font.bold = True  # 加粗
# #     # 设置字体
# #     style.font = font
# #     # 使用样式写入数据
# #     # sheet.write(0, 1, "xxxxx", style)
# #     print('正在存储数据，请勿打开excel')
# #     # 向sheet中写入数据
# #     name_list = ['公司名字', '法定代表人', '联系方式', '注册人资本', '成立时间', '公司地址', '公司邮件']
# #     for cc in range(0, len(name_list)):
# #         sheet1.write(0, cc, name_list[cc], style)
# #     for i in range(0, len(com_name_list)):
# #         sheet1.write(i + 1, 0, com_name_list[i], style)  # 公司名字
# #         sheet1.write(i + 1, 1, peo_name_list[i], style)  # 法定代表人
# #         sheet1.write(i + 1, 2, peo_phone_list[i], style)  # 联系方式
# #         sheet1.write(i + 1, 3, zhuceziben_list[i], style)  # 注册人资本
# #         sheet1.write(i + 1, 4, chenglishijian_list[i], style)  # 成立时间
# #         sheet1.write(i + 1, 5, com_place_list[i], style)  # 公司地址
# #         sheet1.write(i + 1, 6, email_list[i], style)  # 邮件地址
# #     # 保存excel文件，有同名的直接覆盖
# #     workbook.save(r'E:\test.xls')
# #     print('the excel save success')
#
#
#
#
# #用户名 密码
#
# # //*[@id="u"]
# #
# # driver.switch_to.frame("login_frame")
# # driver.find_element_by_id("switcher_plogin").click()
# #
# # driver.find_element_by_xpath("//*[@id='u']").send_keys("1041107644")
# # # driver.find_element_by_xpath("//*[@id='p']").send_keys("gy0824ZY0606")
# # # driver.find_element_by_xpath("//*[@id='login_button']").click()
# # # # elem_pwd.find_element_by_id("login_button").click()
# # time.sleep(5)
# #
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
def start_excel():
    #初始化列名
    caption = ["公司名称", "注册资本", "实缴资本", "经营状态", "成立日期", "统一社会信用代码", "纳税人识别号", "注册号", "组织机构代码", "公司类型", "所属行业", "核准日期",
               "登记机关", "所属地区", "英文名", "曾用名", "经营方式", "人员规模", "营业期限", "企业地址", "经营范围"]
    caption1=np.array(caption).reshape((1,21))
    start_caption = pd.DataFrame(caption1)
    start_caption.to_csv("D:/code/13548777325.csv", mode="a",encoding="utf_8_sig",index=0,header=0)
    #header=0不保留列名,index=0不需要行索引
    #读取搜索的企业名称
    global enterprise_names
    enterprise_name1= pd.read_csv("C:\Users\gyfea\Desktop/test1.csv",header=0) #获取第一列数据
    print type(enterprise_name1)
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

        for enterprise_name in enterprise_names:
            driver = webdriver.Firefox()
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
            driver.find_element_by_class_name("ma_h1").click()

            # sleep(5)
            #因为打开新窗口，因此需要获取并切换窗口句柄
            sleep(2)
            handles = driver.window_handles
            print(len(handles))
            print(handles)
            driver.switch_to_window(handles[-1])

        #结果初始化，并定点取值
            result1=[]
            enterprise_name = driver.find_element_by_css_selector("div.content > div:nth-child(1) > h1:nth-child(1)").text
            result1.append(enterprise_name)
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



            if len(result1)==21:
                result11=np.array(result1).reshape((1,21))
                final_result=pd.DataFrame(result11)
                final_result.to_csv("D:/code/13548777325.csv",mode="a",encoding="utf_8_sig",index=0,header=0)
            driver.quit()


    #报错信息
    except NoSuchElementException as msg:
        print msg
    finally:
        print ctime()
if __name__ == '__main__':

    start_excel()
    open_web()



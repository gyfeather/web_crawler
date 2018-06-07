#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/6/7 8:34
#!@Author ： gyfeather
#!@File :.py


from wordcloud import WordCloud,ImageColorGenerator
from matplotlib import pyplot
from scipy.misc import imread
import jieba
from time import sleep
import os,sys
import re

import numpy as np
import PIL.Image as Image
import itchat

#1.登录微信好友，并计算男女比例
itchat.login()
#爬取自己好友相关信息， 返回一个json文件
friends = itchat.get_friends(update=True)[0:]
male = female = other = 0
#friends[0]是自己的信息，所以要从friends[1]开始
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other +=1
#计算朋友总数
total = len(friends[1:])
#打印出自己的好友性别比例
print("男性好友： %.2f%%" % (float(male)/total*100) + "\n" +
"女性好友： %.2f%%" % (float(female) / total * 100) + "\n" +
"不明性别好友： %.2f%%" % (float(other) / total * 100))

#2.获得好友信息
def get_var(var):
    variable = []
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable

NickName = get_var("NickName")
Sex = get_var('Sex')
Province = get_var('Province')
City = get_var('City')
Signature = get_var('Signature')
from pandas import DataFrame
data = {'NickName': NickName, 'Sex': Sex, 'Province': Province,
        'City': City, 'Signature': Signature}
frame = DataFrame(data)
frame.to_csv('data.csv', index=True)

#3.获取签名内容
siglist = []
for i in friends:
    signature = i["Signature"].strip().replace("span","").replace("class","").replace("emoji","")
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
text = "".join(siglist)

wordlist = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist)
# coloring = np.array(Image.open(r'C:\Users\gyfea\Desktop\123.png'))#black-white
coloring  = imread(r'C:\Users\gyfea\Desktop\123.png')

my_wordcloud = WordCloud(background_color="white",max_words=300,
                         mask=coloring, max_font_size=60,scale=10,
                         font_path=r"C:\Windows\Fonts\simsun.ttc").generate(word_space_split)
image_colors = ImageColorGenerator(coloring)
# pyplot.imshow(my_wordcloud.recolor(color_func=image_colors))
pyplot.imshow(my_wordcloud)
pyplot.axis("off")
pyplot.show()
my_wordcloud.to_file('test1.jpg')


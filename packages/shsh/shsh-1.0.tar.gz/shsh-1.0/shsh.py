#coding:utf-8
#!/usr/bin/python3
import urllib.request   #用于打开 URL 的可扩展库
import zipfile  #ZIP模块
import time #时间的访问和转换
import os   #操作系统接口模块
from bs4 import BeautifulSoup   #解析html
import xlrd #xls文件解析

def stock_code():    #获取股票代码
    print("开始获取股票代码："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    global trading_time
    #c.execute('drop table code')    #删除表格
    c.execute("CREATE TABLE IF NOT EXISTS code (id INTEGER PRIMARY KEY,code TEXT,name TEXT,minimum TEXT)")   #判断表格不存在，创建“股票代码”表格
    #下载文件
    html1 = urllib.request.urlopen('http://47.97.204.47/syl/',timeout=3000)    #下载
    html2 = BeautifulSoup(html1.read(),'html.parser').find_all('a')[-2].get('href') #解析数据//结果：csi20211221.zip

    urllib.request.urlretrieve("http://47.97.204.47/syl/"+html2, html2)  #下载股票代码
    fff = zipfile.ZipFile(html2,"r")
    for fff1 in fff.namelist():  #获取ZIP文档内所有文件的列表名称
        fff.extract(fff1,os.getcwd())   #解压
    fff.close()
    os.remove(html2) #删除文件
    trading_time = html2.replace('.zip','').replace('csi','')	#获取股票交易时间//结果：20211221
    #解析xls文件
    file3 = xlrd.open_workbook("csi"+trading_time+".xls",encoding_override="gb2312")    #打开文件，文件路径
    sheet1 = file3.sheet_by_name('个股数据')   #通过sheet名称获得sheet对象

    sh_sz = ["sh."+i if i[0]=='6' else "sz."+i for i in sheet1.col_values(0)]    #sh或sz
    stock_obtain = list(zip( sh_sz, sheet1.col_values(1)))#获取第1，2列内容转换列表
    del stock_obtain[0]
    print("获取股票代码成功："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))    #获取股票代码
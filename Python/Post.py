# -*- coding: <utf-8> -*-
import os,pycurl,urllib,StringIO,json,time
from sys import *
from bs4 import BeautifulSoup

useragent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"

def login(id, pw):
    loginUrl = "https://bbs.sjtu.edu.cn/bbslogin"
    loginData = {"id":id, "pw":pw}
    crl = pycurl.Curl() 
    crl.setopt(pycurl.URL, loginUrl)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.WRITEFUNCTION, crl.fp.write)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)  
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)  
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(crl.POSTFIELDS,  urllib.urlencode(loginData))
    crl.setopt(pycurl.COOKIEJAR, os.getcwd() + os.sep + "cookies" + os.sep + id + ".txt")
    crl.perform()
    responseContent = crl.fp.getvalue().decode("gbk")
    if u"<title>出错啦</title>" in responseContent:
        print "Login Failed!"
        return False
    else:
        return True
    
def isLogin(id):
    freetalkUrl = "https://bbs.sjtu.edu.cn/bbsdoc?board=freetalk"
    crl = pycurl.Curl() 
    crl.setopt(pycurl.URL, freetalkUrl)
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.WRITEFUNCTION, crl.fp.write)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)  
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)  
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.COOKIEFILE, os.getcwd() + os.sep + "cookies" + os.sep + id + ".txt")
    crl.perform()
    responseContent = crl.fp.getvalue().decode("gbk")
    crl.close()
    if u"<br>ERROR: 错误的讨论区<br>" in responseContent:
        return False
    else:
        return True

def post(id, pw, board, title, text):
    if not isLogin(id):
        if not login(id, pw):     
            print "Post Failed!"
            return False
    crl = pycurl.Curl() 
    postUrl = "https://bbs.sjtu.edu.cn/bbssnd"
    postData = {"board":board, "title":title, "text":text}
    crl.setopt(pycurl.URL, postUrl)
    crl.setopt(crl.POSTFIELDS,  urllib.urlencode(postData))
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.WRITEFUNCTION, crl.fp.write)
    crl.setopt(pycurl.SSL_VERIFYPEER, 0)  
    crl.setopt(pycurl.SSL_VERIFYHOST, 0)  
    crl.setopt(pycurl.USERAGENT, useragent)
    crl.setopt(pycurl.COOKIEFILE, os.getcwd() + os.sep + "cookies" + os.sep + id + ".txt")
    crl.perform()
    crl.close() 
    print "Post Sucessful!"
    return True
    
    
def getCheeregoBoard():
    url = "http://www.cheerego.com/dome_web/guest.php"
    try:
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        board = soup.find("div", id='blackboardID').find("div")
        text = board.get_text()
        return text
    except:
        return ""
    
data = open('config.json', 'r').read()
config = json.loads(data)

id = config["id"]
pw = config["pw"]
board = config["board"]
title = "[" + time.strftime("%Y/%m/%d") + "]" + u"cheerego小黑板"
title = title.encode("gbk")
text = getCheeregoBoard().encode("gbk")
if len(text) > 0:
    post(id, pw, board, title, text)
        
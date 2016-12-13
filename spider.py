#-*-coding:utf8-*-
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')
cookie = {"Cookie": "_T_WM=f06714a7f717f12af49d65dd6e2b2905; UOR=www.liaoxuefeng.com,widget.weibo.com,www.liaoxuefeng.com; SINAGLOBAL=6077018263417.69.1481099617647; ULV=1481099617675:1:1:1:6077018263417.69.1481099617647:; ALF=1483697571; SUB=_2A251Q5DzDeRxGeVM7VsQ-C3OwjuIHXVWzzC7rDV8PUJbkNBeLUWikW2GFYCqfFkk4aY8qbHQB8XxO4AkAw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWuQ2POAuGU-T8mpf47Yu0j5JpX5oz75NHD95Q0eoq4eKn0eo.NWs4DqcjSKsvV9gp4UcLV9GyQMBtt"}

class Spider(object):
  """docstring for Spider"""
  def __init__(self, seed):
    super(Spider, self).__init__()
    #self.cookie = {"Cookie": "_T_WM=f06714a7f717f12af49d65dd6e2b2905; SINAGLOBAL=6077018263417.69.1481099617647; _s_tentry=-; Apache=2377990463652.375.1481303447789; ULV=1481303447918:4:4:4:2377990463652.375.1481303447789:1481301884512; login_sid_t=2e9090ca0a22a123adddaf09ae6ebac5; wvr=6; UOR=www.liaoxuefeng.com,widget.weibo.com,spr_qdhz_bd_baidusmt_weibo_s; ALF=1483925381; SUB=_2A251TyrUDeRxGeVM7VsQ-C3OwjuIHXVWs7acrDV8PUJbkNBeLUbikW1xICDEEkRgTCI0MGEiSvdO3TG9rA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWuQ2POAuGU-T8mpf47Yu0j5NHD95Q0eoq4eKn0eo.NWs4DqcjSKsvV9gp4UcLV9GyQMBtt"}
    self.cookie ={"cookie": "SCF=AuBTL7k1qD9p1j62tE1L7KKi7kFbvVwNjNNEkwHDPYS4T8CKTPmdpMlOjtoJ1YoyW8Ix0-9Smk9rxzRlebYUW5A.; _T_WM=75eac1d5ee3087919c826b43420fac98; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; SUB=_2A251S4cPDeRxGeVM7VsQ-C3OwjuIHXVWtylHrDV6PUJbkdBeLWXtkW2iH3ATwTh5aLRoVbM--9inx2J3_Q..; SUHB=0G0usenV_3HKwU; SSOLoginState=1481635679"}
    self.seed   = seed
    self.fans   = {}
    self.blog   = []
    self.user   = {}
    #self.get_fansnum()

  def get_fansnum(self):
    fansUrl  = 'http://weibo.cn/{}/fans'.format(self.seed)
    fansHtml = requests.get(fansUrl, cookies = self.cookie).content
    fansPage = BeautifulSoup(fansHtml, 'lxml')
    fansnum  = fansPage.findAll('span', class_='tc')[0].text
    self.fansnum = int(fansnum[3:-1])

  def get_blognum(self):
    blogUrl  = 'http://weibo.cn/{}/profile?page=1'.format(self.seed)
    blogHtml = requests.get(blogUrl, cookies=self.cookie).content
    blogPage = BeautifulSoup(blogHtml, 'lxml')
    blogNum  = blogPage.findAll('span', class_='tc')[0].text
    self.blogNum = int(blogNum[3:-1])
    print self.blogNum

  def  get_fans(self):
    pagenum = 19 + 1
    fansFile = open('{}fans.csv'.format(self.seed), 'w')
    fansFile.write(u'用户ID,用户昵称,用户主页链接\n')
    for i in range(1, pagenum+ 1):
      pageUrl = 'http://weibo.cn/{}/fans?page={}'.format(self.seed, i)
      print pageUrl
      pageHtml = requests.get(pageUrl, cookies = self.cookie).content
      pageContent  = BeautifulSoup(pageHtml, 'lxml')
      for fanstable in pageContent.findAll('table'):
        usrname =  fanstable.findAll('a')[-2].text
        usrlink =  fanstable.findAll('a')[-2]['href']
        usrid   =  usrlink[-10:]
        fansFile.write('{},{},{}\n'.format(usrid, usrname, usrlink))
    fansFile.close()

  def get_useinfo(self):
    userUrl = "http://m.weibo.cn/users/{}/?".format(self.seed)
    useHtml = requests.get(userUrl, cookies= self.cookie).content
    userPage = BeautifulSoup(useHtml, 'lxml')
    for info in userPage.findAll('div','item-info-page'):
      self.user[info.span.get_text()] = info.p.get_text()

  def get_blog(self):
    #pagenum = self.blogNum/10 + 1
    pagenum = 354
    print pagenum
    conunt = 1
    zan = []
    transmit = []
    links = []
    blogs = open('blogYuFeng{}.txt'.format(self.seed), "w")
    blogs.write(u'链接,赞,转发,评论,时间,内容概要\n')

    for pageindex in range(1, pagenum+1):
      print 'Page{}'.format(pageindex)
      #http://weibo.cn/2460997447/profile?page=5
      blogUrl  = 'http://weibo.cn/{}/profile?page={}'.format(self.seed, pageindex)
      blogHtml = requests.get(blogUrl, cookies=self.cookie).content
      blogPage = BeautifulSoup(blogHtml, 'lxml')
      
      link = blogPage.findAll('div', class_='c', id=True)
      bloglist = []
      bcount = 0
      for l in link:
        #print l['id']
        address = 'http://m.weibo.com/{}/{}'.format(self.seed ,l['id'][2:])
        detail = l.findAll('span', class_='ctt')[0].text
        like = l.findAll('a')[-4].text
        trans = l.findAll('a')[-3].text
        comment = l.findAll('a')[-2].text
        timeamark = l.findAll('span', class_='ct')[0].text
        #print address, like[2:-1], trans[3:-1], comment[3:-1], timeamark, detail
        print address, like, trans, comment
        for item in l.findAll('a'):
          
          if u'原文评论[' in item.text:
            continue
          #exact comment
          if u'评论[' in item.text:
            comment = item.text[3:-1]
          #exact like
          if u'赞[' in item.text:
            like = item.text[2:-1]
          #exact trans
          if u'转发[' in item.text:
            trans = item.text[3:-1]

        like = str(like)
        like = like.replace('[', '')
        like = like.replace(']', '')
        like = like.replace(u'赞', '')
        blogs.write('{},{},{},{},{},{}\n'.format(address, like, trans, comment, timeamark, detail))
    blogs.close()

if __name__ == '__main__':
  sp = Spider('2714280233')
  sp.get_blog()

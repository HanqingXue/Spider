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

class Spider(object):
  """docstring for Spider"""
  def __init__(self, seed):
    super(Spider, self).__init__()
    self.cookie = {"Cookie": "yourcookie"}
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
    pagenum = self.fansnum/10 + 1
    for i in range(1, pagenum+ 1):
      pageUrl = 'http://weibo.cn/{}/fans?page={}'.format(self.seed, i)
      print pageUrl
      pageHtml = requests.get(pageUrl, cookies = self.cookie).content
      pageContent  = BeautifulSoup(pageHtml, 'lxml')

      for td in pageContent.findAll('td'):
        if len(td.a.get_text()) == 0:
          continue
        else:
          username = td.a.get_text()
          userlink = td.a['href']
          self.fans[username] = userlink
        pass

  def get_useinfo(self):
    userUrl = "http://m.weibo.cn/users/{}/?".format(self.seed)
    useHtml = requests.get(userUrl, cookies= self.cookie).content
    userPage = BeautifulSoup(useHtml, 'lxml')
    for info in userPage.findAll('div','item-info-page'):
      self.user[info.span.get_text()] = info.p.get_text()

  def get_blog(self):
    #pagenum = self.blogNum/10 + 1
    pagenum = 823
    print pagenum
    conunt = 1
    zan = []
    transmit = []
    links = []
    blogs = open('PapiJiangFinally.csv', 'w')
    blogs.write(u'链接,赞,转发,评论,时间,内容概要\n')

    for pageindex in range(1, pagenum+1):
      print 'Page{}'.format(pageindex)
      blogUrl  = 'http://weibo.cn/{}?page={}'.format(self.seed, pageindex)
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
        print like, trans, comment
        blogs.write('{},{},{},{},{},{}\n'.format(address, like, trans, comment, timeamark, detail))
    blogs.close()

if __name__ == '__main__':
  sp = Spider('xiaopapi')
  #sp.get_fansnum()
  #sp.get_fans()
  #sp.get_useinfo()
  #sp.get_blognum()
  sp.get_blog()
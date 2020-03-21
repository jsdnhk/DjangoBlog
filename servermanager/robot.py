#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: robot.py
@time: 2017/8/27 上午1:55
"""

from werobot import WeRoBot
import re
from werobot.replies import ArticlesReply, MusicReply, ImageReply, Article
from .MemcacheStorage import MemcacheStorage
from servermanager.Api.blogapi import BlogApi
from servermanager.Api.commonapi import TuLing
import os
import json
from DjangoBlog.utils import get_md5
from django.conf import settings
import jsonpickle
from servermanager.models import commands

robot = WeRoBot(token=os.environ.get('DJANGO_WEROBOT_TOKEN') or 'lylinux', enable_session=True)
memstorage = MemcacheStorage()
if memstorage.is_available:
    robot.config['SESSION_STORAGE'] = memstorage
else:
    from werobot.session.filestorage import FileStorage
    import os
    from django.conf import settings

    if os.path.exists(os.path.join(settings.BASE_DIR, 'werobot_session')):
        os.remove(os.path.join(settings.BASE_DIR, 'werobot_session'))
    robot.config['SESSION_STORAGE'] = FileStorage(filename='werobot_session')
blogapi = BlogApi()
tuling = TuLing()


def convert_to_articlereply(articles, message):
    reply = ArticlesReply(message=message)
    from blog.templatetags.blog_tags import custom_markdown, truncatechars_content
    from DjangoBlog.utils import CommonMarkdown
    from django.utils.safestring import mark_safe
    for post in articles:
        imgs = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', post.body)
        imgurl = ''
        if imgs:
            imgurl = imgs[0]
        article = Article(
            title=post.title,
            description=truncatechars_content(post.body),
            img=imgurl,
            url=post.get_full_url()
        )
        reply.add_article(article)
    return reply


@robot.filter(re.compile(r"^\?.*"))
def search(message, session):
    s = message.content
    searchstr = str(s).replace('?', '')
    result = blogapi.search_articles(searchstr)
    if result:
        articles = list(map(lambda x: x.object, result))
        reply = convert_to_articlereply(articles, message)
        return reply
    else:
        return '沒有找到相關文章。'


@robot.filter(re.compile(r'^category\s*$', re.I))
def category(message, session):
    categorys = blogapi.get_category_lists()
    content = ','.join(map(lambda x: x.name, categorys))
    return '所有文章分類目錄：' + content


@robot.filter(re.compile(r'^recent\s*$', re.I))
def recents(message, session):
    articles = blogapi.get_recent_articles()
    if articles:
        reply = convert_to_articlereply(articles, message)
        return reply
    else:
        return "暫時還沒有文章"


@robot.filter(re.compile('^help$', re.I))
def help(message, session):
    return '''歡迎關注!
            默認會與圖靈機器人聊天~~
        你可以通過下面這些命令來獲得信息
        ?關鍵字搜索文章.
        如?python.
        category獲得文章分類目錄及文章數.
        category-***獲得該分類目錄文章
        如category-python
        recent獲得最新文章
        help獲得幫助.
        weather:獲得天氣
        如weather:西安
        idcard:獲得身份證信息
        如idcard:61048119xxxxxxxxxx
        music:音樂搜索
        如music:陰天快樂
        PS:以上標點符號都不支持中文標點~~
        '''


@robot.filter(re.compile('^weather\:.*$', re.I))
def weather(message, session):
    return "建設中..."


@robot.filter(re.compile('^idcard\:.*$', re.I))
def idcard(message, session):
    return "建設中..."


@robot.handler
def echo(message, session):
    handler = MessageHandler(message, session)
    return handler.handler()


class CommandHandler():
    def __init__(self):
        self.commands = commands.objects.all()

    def run(self, title):
        cmd = list(filter(lambda x: x.title.upper() == title.upper(), self.commands))
        if cmd:
            return self.__run_command__(cmd[0].command)
        else:
            return "未找到相關命令，請輸入hepme獲得幫助。"

    def __run_command__(self, cmd):
        try:
            str = os.popen(cmd).read()
            return str
        except:
            return '命令執行出錯!'

    def get_help(self):
        rsp = ''
        for cmd in self.commands:
            rsp += '{c}:{d}\n'.format(c=cmd.title, d=cmd.describe)
        return rsp


cmdhandler = CommandHandler()


class MessageHandler():
    def __init__(self, message, session):
        userid = message.source
        self.message = message
        self.session = session
        self.userid = userid
        try:
            info = session[userid]
            self.userinfo = jsonpickle.decode(info)
        except:
            userinfo = WxUserInfo()
            self.userinfo = userinfo

    @property
    def is_admin(self):
        return self.userinfo.isAdmin

    @property
    def is_password_set(self):
        return self.userinfo.isPasswordSet

    def savesession(self):
        info = jsonpickle.encode(self.userinfo)
        self.session[self.userid] = info

    def handler(self):
        info = self.message.content

        if self.userinfo.isAdmin and info.upper() == 'EXIT':
            self.userinfo = WxUserInfo()
            self.savesession()
            return "退出成功"
        if info.upper() == 'ADMIN':
            self.userinfo.isAdmin = True
            self.savesession()
            return "輸入管理員密碼"
        if self.userinfo.isAdmin and not self.userinfo.isPasswordSet:
            passwd = settings.WXADMIN
            if settings.TESTING:
                passwd='123'
            if passwd.upper() == get_md5(get_md5(info)).upper():
                self.userinfo.isPasswordSet = True
                self.savesession()
                return "驗證通過,請輸入命令或者要執行的命令代碼:輸入helpme獲得幫助"
            else:
                if self.userinfo.Count >= 3:
                    self.userinfo = WxUserInfo()
                    self.savesession()
                    return "超過驗證次數"
                self.userinfo.Count += 1
                self.savesession()
                return "驗證失敗，請重新輸入管理員密碼:"
        if self.userinfo.isAdmin and self.userinfo.isPasswordSet:
            if self.userinfo.Command != '' and info.upper() == 'Y':
                return cmdhandler.run(self.userinfo.Command)
            else:
                if info.upper() == 'HELPME':
                    return cmdhandler.get_help()
                self.userinfo.Command = info
                self.savesession()
                return "確認執行: " + info + " 命令?"
        rsp = tuling.getdata(info)
        return rsp


class WxUserInfo():
    def __init__(self):
        self.isAdmin = False
        self.isPasswordSet = False
        self.Count = 0
        self.Command = ''


"""
@robot.handler
def hello(message, session):
    blogapi = BlogApi()
    result = blogapi.search_articles(message.content)
    if result:
        articles = list(map(lambda x: x.object, result))
        reply = convert_to_articlereply(articles, message)
        return reply
    else:
        return '沒有找到相關文章。'
"""

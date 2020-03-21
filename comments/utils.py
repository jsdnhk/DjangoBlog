#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: utils.py
@time: 2018/10/8 10:24 PM
"""

from DjangoBlog.utils import send_email
from DjangoBlog.utils import get_current_site
import logging

logger = logging.getLogger(__name__)


def send_comment_email(comment):
    site = get_current_site().domain
    subject = '感謝您發表的評論'
    article_url = "https://{site}{path}".format(site=site, path=comment.article.get_absolute_url())
    html_content = """
                   <p>非常感謝您在本站發表評論</p>
                   您可以訪問
                   <a href="%s" rel="bookmark">%s</a>
                   來查看您的評論，
                   再次感謝您！
                   <br />
                   如果上面鏈接無法打開，請將此鏈接複製至瀏覽器。
                   %s
                   """ % (article_url, comment.article.title, article_url)
    tomail = comment.author.email
    send_email([tomail], subject, html_content)
    try:
        if comment.parent_comment:
            html_content = """
                    您在 <a href="%s" rel="bookmark">%s</a> 的評論 <br/> %s <br/> 收到回覆啦.快去看看吧
                    <br/>
                    如果上面鏈接無法打開，請將此鏈接複製至瀏覽器。
                    %s
                    """ % (article_url, comment.article.title, comment.parent_comment.body, article_url)
            tomail = comment.parent_comment.author.email
            send_email([tomail], subject, html_content)
    except Exception as e:
        logger.error(e)

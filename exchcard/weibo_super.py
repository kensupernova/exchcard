#coding=utf-8
"""
==================================
function:   基于新浪微博API，对微博登陆进行扩展
addDate:	2014-06-04
author:	 BeginMan
==================================
"""
import datetime
import urllib
import urllib2
import simplejson as json
# import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings

from exchcard.models import XUser


# 默认图片
DEFAULT_PIC = 'http://images.cnitblog.com/news/66372/201405/271116202595556.jpg'

# 用户信息
USER_INFO_URL = 'https://api.weibo.com/2/users/show.json'

# 发送微博
SEND_WEIBO_URL = 'https://api.weibo.com/2/statuses/upload_url_text.json'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
headers = {'User-Agent': user_agent}


class WeiboSuper(object):
    def __init__(self, weibo_access_token, weibo_uid, request=None, **kwargs):
        self.weibo_access_token = weibo_access_token
        self.weibo_uid = weibo_uid
        self.request = request
        self.user_cache = None
        self.kwargs = kwargs

    def create_new_user(self):
        """创建新用户"""
        userInfo = self.get_user_info()
        username = userInfo.get('screen_name', None)
        if XUser.objects.filter(username=username).exists():
            username = username+'[weibo]'

        ## 用户的Id
        newuser_id = 0

        try:
            new_user = XUser.objects.create_user(
                    email=str(self.weibo_uid) + '@weibo.com',
                    username=username,
                    password=self.weibo_uid,

                    type=1, # weibo user
                    weibo_uid=self.weibo_uid,
                    weibo_access_token=self.weibo_access_token,

                    sex=int(userInfo.get('sex', 1)),
                    url=userInfo.get('url', ''),
                    desc=userInfo.get('description', ''),
                    avatar=userInfo.get('avatar_large', '')
            )

            newuser_id = new_user.id
            print(u"success create new user from new weibo auth with user id {0}".format(newuser_id))

            self.login()  # 新用户登陆

        except:
            print(u"fail to create new user from new weibo auth")
            pass

        return newuser_id

    def get_user_info(self):
        """获取微博用户信息"""
        data = {'access_token': self.weibo_access_token, 'uid': self.weibo_uid}

        params = urllib.urlencode(data)

        values = urllib2.Request(USER_INFO_URL+'?%s' %params, headers=headers)
        response = urllib2.urlopen(values)
        result = json.loads(response.read()) # 把string转化为dict对象，与json.dumps把dict对象转化为string

        if result.get('error_code', None):
            # 写入日志
            print(u'获取用户信息失败')
            return False
        return result

    def send_weibo(self):
        """用户发送微博"""
        status = self.kwargs.get('status', None)	   # 微博内容
        visible = self.kwargs.get('visible', 0)	 # 微博的可见性，0：所有人能看，1：仅自己可见，2：密友可见，3：指定分组可见，默认为0。
        url = self.kwargs.get('url', DEFAULT_PIC)   # 配图

        result = {}
        if status:
            data = {'access_token': self.weibo_access_token, 'status': status, 'visible':visible, 'url':url}
            params = urllib.urlencode(data)
            values = urllib2.Request(USER_INFO_URL+'?%s' %params, headers=headers)
            response = urllib2.urlopen(values)
            result = json.loads(response.read())
            if result.get('error_code', None):
                # 写入日志
                print(u'发送微博失败')
                return False
            return True
        return result

    def login(self):
        """登陆"""
        # user_ = XUser.objects.filter(weibo_uid=self.weibo_uid).first()
        user = authenticate(email=str(self.weibo_uid) + '@weibo.com', password=self.weibo_uid)
        login(self.request, user)

    def logout(self):
        """
        注销
        :return:
        """
        logout(self.request)
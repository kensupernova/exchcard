#coding: utf-8
import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.test import APIClient

from exchcard import settings
from exchcard.weibo_super import SuperWeibo
from exchcard.models import XUser
from exchcard.webo_apiclient import APIClient

def weibo_login(request):
    """微博登录"""
    client = APIClient(app_key=settings.APP_KEY,
                       app_secret=settings.APP_SERCET,
                       redirect_uri=settings.CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)


def weibo_check(request):
    code = request.GET.get('code', None) ## 从微博返回后，到回调函数url
    now = datetime.datetime.now()
    if code:
        client = APIClient(app_key=settings.APP_KEY,
                           app_secret=settings.APP_SERCET,
                           redirect_uri=settings.CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token   # 返回的token，类似abc123xyz456
        expires_in = r.expires_in	   # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        uid = r.uid

        # 在此可保存access token
        client.set_access_token(access_token, expires_in)

        request.session['access_token'] = access_token
        request.session['expires_in'] = expires_in
        request.session['uid'] = uid

        user = SuperWeibo(weibo_access_token=access_token, weibo_uid=uid, request=request)	  # 实例化超级微博类

        # 更新数据库
        if XUser.objects.filter(weibo_uid=uid).exists():
            # 用户已经存在
            XUser.objects.filter(weibo_uid=uid).update(last_login=now)
            user.Login()	# 登陆
            return HttpResponseRedirect('/profile')
        else:
            # 创建用户并登陆
            newuser_id = user.createUser()
            if newuser_id:
                # return HttpResponseRedirect('/manage/user/%s/' %u_id)
                return HttpResponseRedirect('/account/address/create/')

    return HttpResponse('/404/')
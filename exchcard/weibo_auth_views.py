#coding: utf-8
import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.test import APIClient

from exchcard import settings
from exchcard.weibo_super import WeiboSuper
from exchcard.models import XUser
from exchcard.weibo_apiclient import APIClient


def weibo_auth(request):
    """微博登录"""
    client = APIClient(app_key=settings.APP_KEY,
                       app_secret=settings.APP_SERCET,
                       redirect_uri=settings.CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)


def weibo_auth_callback(request):
    code = str(request.GET.get('code', None)) ## 从微博登录返回后，到回调函数url, 会带有?code=parameter
    print(u"微博成功登录返回后得到的code为 %s" % code)
    if code:
        print(u"code is not none")
    else:
        return HttpResponse("Fail to log in with weibo, try local log in!")

    now = datetime.datetime.utcnow()
    client = APIClient(app_key=settings.APP_KEY,
                       app_secret=settings.APP_SERCET,
                       redirect_uri=settings.CALLBACK_URL)
    r = client.request_access_token(code)
    print(u"use code: {0} to get access token: {1}".format(code, r))

    access_token = r.access_token  # 返回的token，类似abc123xyz456
    uid = r.uid
    expires_in = r.expires_in  # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    expires = r.expires # expires_in = expires
    print(u'access token:{0}, uid:{1}, expires in :{2}, expires :{3}, '.
          format(access_token, uid, expires_in, expires))

    # 在此可保存access token
    client.set_access_token(access_token, expires)

    # save information in request session
    request.session['access_token'] = access_token
    request.session['expires_in'] = expires_in
    request.session['uid'] = uid
    request.session['expires'] = expires

    # information to be used by server side
    weibo_super = WeiboSuper(weibo_access_token=access_token, weibo_uid=uid, request=request)  # 实例化超级微博类

    # 查找数据库
    if XUser.objects.filter(weibo_uid=uid).exists():
        # 如果用户已经存在
        XUser.objects.filter(weibo_uid=uid).update(last_login=now)
        weibo_super.login()  # 登陆, 然后进入个人主页
        return HttpResponseRedirect('/profile')
    else:
        # 如果不存在，创建用户并登陆
        newuser_id = weibo_super.create_new_user()
        # print(u'new user id is {0}'.format(newuser_id))
        if newuser_id:
            # newly created user has no profile
            return HttpResponseRedirect('/account/address/create/')
            # return HttpResponseRedirect('/profile/')
        else:
            return HttpResponse(u"Fail to create new user with weibo auth information")


def weibo_auth_cancel(request):
    """
    当用户取消授权，微博开放平台调用该地址, 登录退出
    :param request:
    :return:
    """
    client = APIClient(app_key=settings.APP_KEY,
                       app_secret=settings.APP_SERCET,
                       redirect_uri=settings.CALLBACK_URL)
    client.logout()

    return HttpResponseRedirect("/")
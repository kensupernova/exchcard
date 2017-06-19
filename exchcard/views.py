#coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from exchcard.models_main import Card, CardPhoto, Profile


def index(request):
    return render(request, 'exchcard/index.html')


def about(request):
    if request.user.is_authenticated():
        context = {
            "user": request.user,
            "isAuth": True
        }
        try:
            p = Profile.objects.get(profileuser=request.user)
            context['profile'] = p
        except Profile.DoesNotExist:
            context['profile'] = None

        return render(request, 'exchcard/about-page.html', context)
    else:
        return render(request, 'exchcard/about-page.html')


def user_login(request):
    return render(request, 'exchcard/login.html')


def user_register(request):
    return render(request, 'exchcard/user-register-page.html')


@login_required
def address_create(request):
    if Profile.objects.filter(profileuser=request.user).exists():
        """
        如果用户的profile已经建立，address已经填写，直接进入个人页面
        """
        print(u"profile exists!")
        return HttpResponseRedirect(redirect_to="/profile/")

    context = {
        "user": request.user,
        "isAuth": True
    }

    print(u"no address, no profile, render address create page!")

    return render(request, 'exchcard/address-create-page.html', context)


# 注入登录验证
@login_required
def profile_view(request):
    try:
        p = Profile.objects.get(profileuser=request.user)
        context = {'profile': p, 'user': request.user, 'isAuth': True}
        return render(request, 'exchcard/profile-page.html', context)

    except Profile.DoesNotExist:
        return HttpResponseRedirect(redirect_to="/account/address/create/")


@login_required
def setting(request):
    """
    设置, 包括账户User, 地址Address, 主页Profile, 头像Avatar
    :param request:
    :return:
    """
    try:
        p = Profile.objects.get(profileuser=request.user)
        context = {"profile": p, "user": request.user}
        context['isAuth'] = True
        return render(request, 'exchcard/setting-page.html', context)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(redirect_to="/account/address/create/")


@login_required
def account_setting(request):
    """
    账户设置
    :param request:
    :return:
    """
    profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile, 'user': request.user}
    context['isAuth'] = True
    return render(request, 'exchcard/account-setting-page.html', context)





@login_required(login_url="/account/login")
def card_send(request):
    profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile, 'user': request.user}
    context['isAuth'] = True
    return render(request, 'exchcard/send-card-page.html', context)


@login_required
def card_send_confirm(request):
    profile = Profile.objects.get(profileuser
                                            =request.user)

    context = {'profile': profile, 'user': request.user}
    context['isAuth'] = True

    return render(request, 'exchcard/send-card-page.html', context)

"""
查看某张在路途中的明信片
"""
@login_required
def card_travelling(request, cardname):
    """
    view the travelling card with name
    :param request:
    :param cardname:
    :return: view
    """
    try:
        card = Card.objects.get(card_name=cardname)
    except Card.DoesNotExist:
        context = {
            'card_name': cardname
        }
        return render(request, 'exchcard/error/card-does-not-exist-page.html', context)

    if card.has_arrived:
        context = {
            'card_name': cardname,
            'has_arrived': True,
            'next':'/card/' + cardname
        }
        return render(request, 'exchcard/error/card-has-arrived-page.html', context)

    context = {'card_name':cardname,
               'recipient_user':card.torecipient.profileuser,
               'recipient_address': card.torecipient.profileaddress,
               'card': card
               }
    context['profile'] = Profile.objects.get(profileuser=request.user)
    context['user'] = request.user
    context['isAuth'] = True

    card_photos = CardPhoto.objects.filter(card_host=card)
    if card_photos.count() > 0:
        context['card_photos'] = card_photos
    else:
        print u"not card photos of card %s" % cardname

    return render(request, 'exchcard/travelling-card-page.html', context)


@login_required
def card_receive(request):
    profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile, 'user': request.user}
    context['isAuth'] = True
    if request.method == "GET":
        return render(request, 'exchcard/receive-card-page.html', context)


"""
查看某张明信片
"""
@login_required
def view_single_card(request, cardname):
    """
    view the travelling card with name
    :param request:
    :param cardname:
    :return: view
    """

    try:
        card = Card.objects.filter(card_name=cardname).first()
    except:
        return HttpResponse(json.dumps({
            "details": "server error!"
        }))

    context = {'card_name':cardname,
               'recipient_user':card.torecipient.profileuser,
               'recipient_address': card.torecipient.profileaddress,
               'card': card}

    context['profile'] = Profile.objects.get(profileuser=request.user)
    context['user'] = request.user
    context['isAuth'] = True

    card_photos = CardPhoto.objects.filter(card_host=card)
    if card_photos.count()>0:
        context['card_photos'] = card_photos
    else:
        print "not card photos of card %s" % cardname

    return render(request, 'exchcard/single-card-page.html', context)


"""
查看明信片列表
"""
@login_required
def view_cards_list(request):
    profile = Profile.objects.get(profileuser
                                            =request.user)
    context= {}
    context['profile'] = profile
    context['user'] = request.user
    context['isAuth'] = True
    return render(request, 'exchcard/view-cards-page.html', context)



@login_required
def hobbyist_list(request):
    profile = Profile.objects.get(profileuser
                                               =request.user)

    context = {'profile':profile }
    context['user'] = request.user
    context['isAuth'] = True
    return render(request, 'exchcard/hobbyist-list-page.html', context=context)



@login_required
def eachs_public_profile(request, user_id):
    """
    浏览其他用户的主页
    :param request:
    :param username:
    :return:
    """
    profile = Profile.objects.get(profileuser
                                  =request.user)

    context = {}
    context['profile'] = profile
    context['user'] = request.user
    context['isAuth'] = True
    return render(request, 'exchcard/public-profile-page.html', context)


@login_required
def view_shao_you_quan(request):
    """
    烧友圈
    :param request:
    :return:
    """
    profile = Profile.objects.get(profileuser
                                  =request.user)

    context = {}
    context['profile'] = profile
    context['user'] = request.user
    context['isAuth'] = True
    return render(request, 'exchcard/moments-page.html', context=context)



#coding: utf-8

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render

from exchcard.models_profile import Card, CardPhoto, Profile


def index(request):
    return render(request, 'index.html')


def user_login(request):
    return render(request, 'login.html')


def user_register(request):
    return render(request, 'exchcard/user-register-page.html')


@login_required
def address_create(request):
    if request.user.is_authenticated():
        context = {
            "user": request.user
        }

        return render(request, 'exchcard/address-create-page.html', context)
    else:
        return Http404


@login_required
def setting(request):
    """
    设置, 包括账户User, 地址Address, 主页Profile, 头像Avatar
    :param request:
    :return:
    """
    profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile}
    return render(request, 'exchcard/setting-page.html', context)


@login_required
def account_setting(request):
    """
    账户设置
    :param request:
    :return:
    """
    profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile}
    return render(request, 'exchcard/account-setting-page.html', context)


## 注入登录验证
@login_required
def profile(request):
    try:
        profile_from_request = Profile.objects.get(profileuser=request.user)
        context = {'profile': profile_from_request}
        return render(request, 'exchcard/profile-page.html', context)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(redirect_to="/account/address/create/")


@login_required(login_url="/account/login")
def card_send(request):
    logged_profile = Profile.objects.get(profileuser=request.user)
    context = {'profile': logged_profile}

    return render(request, 'exchcard/send-card-page.html', context)


@login_required
def card_send_confirm(request):
    profile_from_request = Profile.objects.get(profileuser
                                            =request.user)

    context = {}

    if request.data["send_postcard"]:
        context['profile']= profile_from_request

    return render(request, 'exchcard/send-card-page.html', context)


@login_required
def card_receive(request):
    profile_of_request = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile_of_request}

    if request.method == "GET":
        return render(request, 'exchcard/receive-card-page.html', context)


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
    card = Card.objects.get(card_name=cardname)
    context = {'card_name':cardname,
               'recipient_user':card.torecipient.profileuser,
               'recipient_address': card.torecipient.profileaddress
               }
    context['profile'] = Profile.objects.get(profileuser=request.user)

    return render(request, 'exchcard/travelling-card-page.html', context)


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

    card = Card.objects.get(card_name=cardname)

    context = {'card_name':cardname,
               'recipient_user':card.torecipient.profileuser,
               'recipient_address': card.torecipient.profileaddress}
    context['profile'] = Profile.objects.get(profileuser=request.user)

    try:
        cardphoto = CardPhoto.objects.get(card_host=card)
        context["url"] = cardphoto.card_photo.url
    except:
        ''
    return render(request, 'exchcard/travelling-card-page.html', context)


"""
查看明信片列表
"""
@login_required
def view_cards_list(request):
    profile_from_request = Profile.objects.get(profileuser
                                            =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/view-cards-page.html', context)




def hobbyist_list(request):
    profile_from_request = Profile.objects.get(profileuser
                                               =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/hobbyist-list-page.html', context=context)



@login_required
def eachs_public_profile(request, user_id):
    """
    浏览其他用户的主页
    :param request:
    :param username:
    :return:
    """
    profile_from_request = Profile.objects.get(profileuser
                                               =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/public-profile-page.html', context)


@login_required
def view_shao_you_quan(request):
    """
    烧友圈
    :param request:
    :return:
    """
    profile_from_request = Profile.objects.get(profileuser
                                               =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/moments-page.html', context=context)


def about(request):
    profile_from_request = Profile.objects.get(profileuser
                                               =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/about-page.html', context=context)

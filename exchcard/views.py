#coding: utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from exchcard.models import Card, CardPhoto, Profile


def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_register(request):
    return render(request, 'exchcard/user-address-register-page.html')

## 注入验证
@login_required
def profile(request):
    profile_from_request = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile_from_request}
    return render(request, 'exchcard/profile-page.html', context)

@login_required
def card_send(request):
    profile_from_request = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile_from_request}

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
def card_register(request):
    profile_from_request = Profile.objects.get(profileuser=request.user)
    context = {'profile': profile_from_request}

    if request.method == "GET":
        return render(request, 'exchcard/receive-card-page.html', context)

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

@login_required
def view_cards_list(request, id):
    profile_from_request = Profile.objects.get(profileuser
                                            =request.user)

    context = {'profile': profile_from_request}

    return render(request, 'exchcard/view-cards-page.html', context)

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

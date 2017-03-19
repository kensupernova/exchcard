#coding: utf-8
import re
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

from exchcard.models import Card, CardPhoto, Profile

from mysite.forms import RegisterCardForm

def home(request):
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

    # if request.method == "POST":
    #     card_name = request.POST['card_name']
    #     print card_name
    #     ## check whether the card recipient id == request user
    #     try:
    #         card = Card.objects.get(card_name = card_name)
    #     except Card.DoesNotExist:
    #         return HttpResponse({"details card name %s is invalid" % card_name})
    #
    #     ## has_arrived is true, respond with ok
    #     if card.has_arrived:
    #         return HttpResponse({"details %s already registered" % card_name})
    #
    #
    #     profile_request = Profile.objects.get(profileuser=request.user)
    #     if card.torecipient.id == profile_request.id:
    #         card.mark_arrived()
    #
    #         return render(request, 'exchcard/view-card-page.html', {'card': card, 'profile': profile_from_request})
    #
    #     else:
    #         return HttpResponse({"details errors: request user id != card recipient id"})

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

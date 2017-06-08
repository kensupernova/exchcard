# -*- coding: utf-8 -*-

from exchcard.models_main import Card,CardPhoto, Profile, SentCardAction
from exchcard.models_main import DianZan
from exchcard_backend_api.serializers import DianZanSerializer, SentCardActionSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# All the dianzan of a postcard
class DianzanListView(generics.ListAPIView):
    serializer_class = DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        cardid = self.kwargs['cardid']
        card = Card.objects.filter(id=int(cardid))
        return DianZan.objects.filter(card_by_dianzan=card)


class DianzanRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DianZan.objects.all()
    serializer_class =  DianZanSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class SentCardActionListView(generics.ListAPIView):
    serializer_class = SentCardActionSerializer
    permission_classes = [permissions.IsAuthenticated,  ]
    queryset = SentCardAction.objects.all()


class SentCardActionDetailView(generics.RetrieveAPIView):
    queryset = SentCardAction.objects.all()
    serializer_class = SentCardActionSerializer

    lookup_field = ["pk"]

    permission_classes = [
        permissions.IsAuthenticated
    ]

##################################################
### add dianzan to a card
@api_view(["GET", "POST", "PUT", "DELETE",  ])
@permission_classes([permissions.IsAuthenticated,])
def card_dianzan(request, cardid, photoid):
    profile_from_user = Profile.objects.get(profileuser=request.user)

    try:
        card = Card.objects.get(id=int(cardid))
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        cardphoto = CardPhoto.objects.get(id=int(photoid))
    except CardPhoto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if request.method == 'POST':
        card_by_dianzan_id = card.id,
        person_who_dianzan_id = profile_from_user.id

        ## check whether had been dianzan already
        if DianZan.objects.filter(person_who_dianzan = profile_from_user,
                                  card_by_dianzan = card,
                                  card_photo_by_dianzan = cardphoto).exists():
            # DianZan.objects.filter(person_who_dianzan = profile_from_user, card_by_dianzan = card).delete()
            return Response({"detail": "already dianzan"})

        else:
            zan = DianZan.objects.create_with_ids(card_by_dianzan_id=card.id,
                                                  card_photo_by_dianzan_id=cardphoto.id,
                                                person_who_dianzan_id=profile_from_user.id)
            serializer = DianZanSerializer(zan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "PUT":
        ## check whether had been dianzan already
        if DianZan.objects.filter(person_who_dianzan=profile_from_user, card_by_dianzan=card).exists():
            # DianZan.objects.filter(person_who_dianzan=profile_from_user, card_by_dianzan=card).delete()
            return Response({"detail": "Already dianzan"})

        else:
            zan = DianZan.objects.create_with_ids(card_by_dianzan_id=card.id,
                                                  person_who_dianzan_id=profile_from_user.id)

            serializer = DianZanSerializer(zan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    if request.method == "DELETE":
        zan = DianZan.objects.filter(card_by_dianzan_id = data['card_by_dianzan_id'])
        zan.delete()

    if request.method == 'GET':
        zan = DianZan.objects.filter(card_by_dianzan_id=data['card_by_dianzan_id'])
        serializer = DianZanSerializer(zan)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated,])
def card_dianzans(request, cardid):
    cardid = int(cardid)
    try:
        card = Card.objects.get(id=cardid)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        zans = DianZan.objects.filter(card_by_dianzan_id =cardid)
        results = [obj.as_json() for obj in zans]
        return Response(results, status= status.HTTP_200_OK)

#

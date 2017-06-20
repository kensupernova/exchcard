#coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render

from exchcard.forms import UploadFileForm
from exchcard.models_main import Profile, AvatarPhoto
from utils import utils


def upload_file_view(request):
    if request.method == "POST":
        # print "deal with post request"
        # print request.POST
        # print request.FILES
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES['file']
            # title = request.POST["title"]

            # ## Handled by model with filefiled or imagefield
            # ## File is saved to MEDIA_ROOT/upload_to or storage root/upload_to
            # ## upload_to is a parameter when creating the model
            profile = Profile.objects.get(profileuser = request.user)
            # 改变文件的名字
            f.name = utils.hash_file_name(f.name)
            instance = AvatarPhoto(owner = profile, avatar=f)
            instance.save()

            return HttpResponse('image upload success')
            ## or redirect to succuess url
            # return HttpResponseRedirect("/main/upload/success")

        else:
            print (u"form is invalid")

    elif request.method == "GET":
        form = UploadFileForm()
        return render(request, 'upload_file_page.html', {'form':form})



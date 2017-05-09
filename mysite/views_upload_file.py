from django.http import HttpResponse
from django.shortcuts import render

from mysite.forms import UploadFileForm
from mysite import settings

from exchcard_backend_api import utils
from exchcard_backend_api.models import Profile, AvatarPhoto

def uploadFile(request):
    if request.method == "POST":
        # print "deal with post request"
        # print request.POST
        # print request.FILES
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES['file']
            title = request.POST["title"]
            # method 1: handle manually
            # utils.handle_uploaded_file(title, f)

            # ## method 2: handle by model with filefiled or imagefield
            # ## file is saved to MEDIA_ROOT/upload_to or storage root/upload_to
            exchcard= Profile.objects.get(profileuser = request.user)
            instance = AvatarPhoto(owner = exchcard, avatar=f)
            instance.save()

            return HttpResponse('image upload success')
            ## or redirect to succuess url
            # return HttpResponseRedirect("/api/exchcard_backend_api/profiles/")

        else:
            print "form is invalid"

    else:
        form = UploadFileForm()
    return render(request, 'mainpage.html', {'form':form})



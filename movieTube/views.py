from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from movieTube.form import SignUpForm
from videos.models import VideoInfo


def index(request):
    template_name = loader.get_template('./index.html')
    context_object_name = 'video_list'

    queryset = VideoInfo.objects.all().order_by('-publish_date')
    context = {
        context_object_name: queryset
    }
    for i in queryset:
        print(i.id)
    return HttpResponse(template_name.render(context, request))


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/videos')
    else:
        form = SignUpForm()
    return render(request, './signup.html', {'form': form})

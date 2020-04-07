from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import SurveyForm
from .models import VideoInfo
import os

from movieTube import  settings
from .models import VideoInfo, VideoCategory


def index(request):
    template = loader.get_template('./index.html')
    context_object_name = 'video_list'
    search_query = ""
    cat_query = ""

    if request.method == 'GET':
        if request.GET.get('search', ""):
            search_query = request.GET.get('search', "")
        else:
            cat_query = request.GET.get('cat', "")

    if search_query:
        queryset = VideoInfo.objects.filter(name__icontains=search_query).order_by('-publish_date')
    elif cat_query:
        queryset = VideoInfo.objects.filter(content_type__contains=cat_query).order_by('-publish_date')
    else:
        queryset = VideoInfo.objects.all().order_by('-publish_date')
    context = {
        context_object_name: queryset
    }
    for i in queryset:
        print(i.id)
    return HttpResponse(template.render(context, request))


def detail(request, pk):
    template = './detail.html'
    context_object_name = 'video'

    video = VideoInfo.objects.get(id=pk)
    video.view_count += 1
    video.save()
    video.view_count = round(video.view_count/2)
    video_list = VideoInfo.objects.filter(content_type=video.content_type).order_by('-publish_date')
    context = {
        context_object_name: video,
        'video_list': video_list,
    }

    return render(request, template, context)


def survey(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SurveyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            request.session['device'] = form.data['device_type']
            request.session['quality'] = form.data['quality']
            return HttpResponseRedirect('/videos/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SurveyForm()

    return render(request, 'survey.html', {'form': form})

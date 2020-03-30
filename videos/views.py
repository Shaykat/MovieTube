from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import VideoInfo
import os

from movieTube import  settings
from .models import VideoInfo, VideoCategory


def index(request):
    template = loader.get_template('./index.html')
    context_object_name = 'video_list'

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
    context = {
        context_object_name: video
    }

    return render(request, template, context)

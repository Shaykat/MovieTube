from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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
    return HttpResponse(template.render(context, request))

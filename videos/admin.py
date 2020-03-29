from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import VideoCategory, VideoInfo

admin.site.register(VideoCategory)
admin.site.register(VideoInfo)

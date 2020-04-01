from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import VideoCategory, VideoInfo


class VideoInfoAdmin(admin.ModelAdmin):
    actions = ['encode']
    list_display = ('name', 'content_type', 'video_rating', 'modified_date')
    ordering = ('-modified_date',)

    class Meta:
        model = VideoInfo

    def encode(self, request, queryset):
        p = request
        print("Encoded")



admin.site.register(VideoCategory)
admin.site.register(VideoInfo)

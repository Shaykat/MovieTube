from django.contrib import admin

from .models import VideoCategory, VideoInfo


class VideoInfoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information',               {'fields': ['name', 'description', 'content_type', 'categories', 'video_rating', 'class_name']}),
        ('User Information',               {'fields': ['author', 'allow_comments', 'is_public', 'view_count']}),
        ('Content',               {'fields': ['videofile', 'cover_img', 'low_quality_url', 'medium_quality_url', 'high_quality_url']}),
        ('Date information', {'fields': ['upload_datetime', 'publish_date']}),
    ]
    list_display = ('name', 'description', 'content_type', 'publish_date', 'author', 'view_count')
    list_filter = ['publish_date', 'content_type', 'video_rating', 'view_count']


admin.site.register(VideoCategory)
admin.site.register(VideoInfo, VideoInfoAdmin)

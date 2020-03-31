from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from import_export import resources
import PIL

CONTENT_TYPES = (
    ('song', 'Song'),
    ('movie', 'Movie'),
    ('blog', 'Blog'),
    ('tutorial', 'Tutorial'),
    ('drama', 'Drama'),
)


class VideoCategory(models.Model):
    """ A model to help categorize videos """
    title = models.CharField(max_length=255)
    # slug = models.SlugField(
    #     null=True
    # )
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Video Categories"

    def __unicode__(self):
        return "%s" % self.title

    def __str__(self):
        return self.title

    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return 'videostream_category_detail', [self.slug]


class VideoInfo(models.Model):
    name = models.CharField('Name', max_length=200)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name="Video")
    description = models.CharField('Description', max_length=400)
    upload_date = models.DateField(auto_now_add=True)
    upload_datetime = models.DateTimeField('Upload Date Time')
    content_type = models.CharField('Content Type', max_length=20, choices=CONTENT_TYPES, default='song')
    # content_path = models.SlugField(unique=True, help_text="A url friendly slug for the video clip.")
    categories = models.ManyToManyField(VideoCategory)
    categories = models.ManyToManyField(VideoCategory)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=False)
    video_rating = models.FloatField('Video Rating', null=True)
    cover_img = models.ImageField('Cover Image', upload_to="", null=True)
    class_name = models.IntegerField('Class Name', null=True)

    # TODO:
    #  In future we may want to allow for more control over publication
    is_public = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    def content_path(self):
        return slugify(self.name)

    def __str__(self):
        return self.name + ": " + str(self.videofile)

    class Meta:
        ordering = ('-publish_date', '-upload_date')
        get_latest_by = 'upload_date'

    def __unicode__(self):
        return "%s" % self.name

    def was_published_recently(self):
        return self.upload_datetime >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return ('videostream_video_detail', (), {
            'year': self.publish_date.strftime("%Y"),
            'month': self.publish_date.strftime("%b"),
            'day': self.publish_date.strftime("%d"),
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        self.modified_date = datetime.now()
        if self.publish_date is None and self.is_public:
            self.publish_date = datetime.now()
        super(VideoInfo, self).save(*args, **kwargs)


# class HTML5Video(models.Model):
#     OGG = 0
#     WEBM = 1
#     MP4 = 2
#     FLASH = 3
#     VIDEO_TYPE = (
#         (OGG, 'video/ogg'),
#         (WEBM, 'video/webm'),
#         (MP4, 'video/mp4'),
#         (FLASH, 'video/flv'),
#     )
#
#     video_type = models.IntegerField(
#         choices=VIDEO_TYPE,
#         default=WEBM,
#         help_text="The Video type"
#     )
#     video_file = models.FileField(
#         upload_to="videos/html5/",
#         help_text="The file you wish to upload. Make sure that it's the correct format.",
#     )
#
#     # Allow for multiple video types for a single video
#     # basic_video = models.ForeignKey(BasicVideo)
#
#     class Meta:
#         verbose_name = "Html 5 Video"
#         verbose_name_plural = "Html 5 Videos"
#
#
# class EmbedVideo(VideoInfo):
#     video_url = models.URLField(null=True, blank=True)
#     video_code = models.TextField(
#         null=True,
#         blank=True,
#         help_text="Use the video embed code instead of the url if your frontend does not support embedding with the URL only."
#     )

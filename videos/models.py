from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import subprocess
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
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    allow_comments = models.BooleanField(default=False)
    video_rating = models.FloatField('Video Rating', null=True, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    cover_img = models.ImageField('Cover Image', upload_to="", null=True)
    class_name = models.IntegerField('Class Name', null=True, default=0)
    low_quality_url = models.CharField('Low Quality Video URL', null=True, blank=True, max_length=200)
    medium_quality_url = models.CharField('Medium Quality Video URL', null=True, blank=True, max_length=200)
    high_quality_url = models.CharField('High Quality Video URL', null=True, blank=True, max_length=200)

    # TODO:
    #  In future we may want to allow for more control over publication
    is_public = models.BooleanField(default=False)
    is_encoded = models.IntegerField('Is Encoded', null=True, default=0)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField('View Count', null=True, default=0)

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
        cls = ""
        self.modified_date = datetime.now()
        if self.publish_date is None and self.is_public:
            self.publish_date = datetime.now()
        w = .119609736
        b = .21622217
        if (w*self.video_rating) + b >= .65:
            self.class_name = 1
            cls = 'Hot'
        else:
            self.class_name = 0
            cls = 'Cold'
        self.low_quality_url = '/Users/mutalabshaykat/Documents/MM802/media/videos/' + cls + '/low/' + str(self.videofile)
        self.medium_quality_url = '/Users/mutalabshaykat/Documents/MM802/media/videos/' + cls + '/medium/' + str(self.videofile)
        self.high_quality_url = '/Users/mutalabshaykat/Documents/MM802/media/videos/' + cls + '/high/' + str(self.videofile)
        self.is_encoded += 1
        super(VideoInfo, self).save(*args, **kwargs)
        if self.videofile:
            if self.is_encoded <= 0:
                # self.update(is_encoded=True)
                if self.class_name == 1:
                    # var = subprocess.call(['ffmpeg', '-i', '/Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=360:-1', '/Users/mutalabshaykat/Documents/MM802/media/videos/Hot/low/' + str(self.videofile)[7:]])

                    var = subprocess.call(['ffmpeg', '-i', '/Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=480:-1', '/Users/mutalabshaykat/Documents/MM802/media/videos/Hot/medium/' + str(self.videofile)[7:]])

                    # var = subprocess.call(['ffmpeg', '-i', '/Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=720:-1', '/Users/mutalabshaykat/Documents/MM802/media/videos/Hot/high/' + str(self.videofile)[7:]])
                else:
                    # var = subprocess.call(['ffmpeg', '-i', 'Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=360:-1', 'Users/mutalabshaykat/Documents/MM802/media/videos/Cold/low/' + str(self.videofile)[7:]])

                    var = subprocess.call(['ffmpeg', '-i', '/Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=480:-1', '/Users/mutalabshaykat/Documents/MM802/media/videos/Cold/medium/' + str(self.videofile)[7:]])

                    # var = subprocess.call(['ffmpeg', '-i', '/Users/mutalabshaykat/Documents/MM802/media/' + str(self.videofile), '-vf', 'scale=720:-1', '/Users/mutalabshaykat/Documents/MM802/media/videos/Cold/high/' + str(self.videofile)[7:]])

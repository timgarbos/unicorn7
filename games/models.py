from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    short_description = models.TextField('short description')
    short_credits = models.TextField()
    playable_link = models.URLField()
    download_link = models.URLField()
    video_link = models.URLField()
    #developer_link = models.URLField()
    #screenshot = models.ImageField()
    users = models.ManyToManyField(User)
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.title
    
class FrontpagePeriod(models.Model):
	game = models.ForeignKey(Game)
	start_date = models.DateTimeField('start of period')
	end_date = models.DateTimeField('end of period')
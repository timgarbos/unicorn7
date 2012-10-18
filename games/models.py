from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.

class GameCategory(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255,help_text='internal note: Why do we have this category? ')

    def __unicode__(self):
        return self.title

class GamePlatform(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title




class Game(models.Model):
    title = models.CharField(max_length=130)
    pub_date = models.DateTimeField('date published')
    short_description = models.CharField('Short teaser',max_length=130,help_text='Example: This is an erotic rythm game. Do not miss this')
    long_description = models.TextField('description',help_text='Example: it is a game about ... and it is great because of ... you should try it out. (if you would want to write the story of your life then this is the place)')
    short_credits = models.TextField('credits',help_text='Example: It was made by Tim Garbos and Julie Heyde. Thanks to Patrick for the moaning sound effects')
    video = models.URLField(help_text='Optional video (youtube, vimeo, etc) link',null=True,blank=True)
    twitter = models.CharField('twitter id',max_length=100,blank=True)
    developer_url = models.URLField()
    email = models.EmailField()

    users = models.ManyToManyField(User,null=True,blank=True)
    tags = TaggableManager(blank=True)

    categories = models.ManyToManyField(GameCategory,null=True,blank=True)
    platforms = models.ManyToManyField(GamePlatform, through='GamePlatformLink',null=True,blank=True)
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "games"

    @classmethod
    def create(cls, title):
        game = cls(title=title)
        # add default links

        return game


class GamePlatformLink(models.Model):
    game = models.ForeignKey(Game)
    platform = models.ForeignKey(GamePlatform)
    url = models.URLField()

    def __unicode__(self):
        return self.url

class FrontpagePeriod(models.Model):
    game = models.ForeignKey(Game)
    start_date = models.DateTimeField('start of period')
    end_date = models.DateTimeField('end of period')


class GameImage(models.Model):
    game = models.ForeignKey(Game)
    caption = models.CharField(max_length=200)
    #image = models.ImageField('upload_to'='uploads')

    def __unicode__(self):
        return self.caption


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ('pub_date','users','categories','platforms','video','twitter')

class ContactForm(ModelForm):
    class Meta:
        model = Game
        include = ('email','twitter','developer_url')


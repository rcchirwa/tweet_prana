from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User)
    tweet = models.CharField(max_length=140, blank=False)
    status = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, tweet,user,status):
        tweet = cls(tweet=tweet,user=user,status=status)
        return tweet


# Create your models here.

class TweetDetails(models.Model):
    tweet = models.ForeignKey(Tweet)
    id_str = models.CharField(max_length=140, blank=False) 
    html = models.CharField(max_length=512, blank=False)
    stripped_html = models.CharField(max_length=512, blank=False)
    retweet_count = models.IntegerField(max_length=20, blank=False)
    created_at_epoch = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls,tweet, id_str, created_at, created_at_epoch, retweet_count, html, stripped_html):
        tweetDetails = cls(tweet=tweet, id_str=id_str, created_at=created_at, created_at_epoch=created_at_epoch, retweet_count=retweet_count, html=html, stripped_html=stripped_html)
        return tweetDetails



class DirtyWord(models.Model):
    word = models.CharField(max_length=512, blank=False)
    #created_by_user = models.ForeignKey(User)
    #updated_by_user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.word


class PCBrandTerm(models.Model):
    pcTerm = models.CharField(max_length=512, blank=False)
    #created_by_user = models.ForeignKey(User)
    #updated_by_user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.pcTerm


class BrandSensitiveTerm(models.Model):
    pcTerm = models.ForeignKey(PCBrandTerm)
    brandSensitiveTerm = models.CharField(max_length=512, blank=False)
    #created_by_user = models.ForeignKey(User)
    #updated_by_user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.brandSensitiveTerm
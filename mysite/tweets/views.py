# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required#, user_passes_test
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from django.core import serializers
from django.utils import simplejson

from datetime import datetime
from mysite.tweets.models import Tweet, TweetDetails

import math
import logging
import json
import tweet_handler





#this is the the landing page and it process the login sequance as well 
def landing(request): 
    template_out = ""

    if request.method == 'GET':
        #straight get renders the page
        template_out = 'login.html'
    elif request.method == 'POST':
        #The Post authenticates the user
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            pass

        #authenticate the user
        user = authenticate(username=username, password=password)


        template_out = "tweet.html"
        if user is not None:
            #if the authentication was a sucess log the user in to enable session attributes and use of the user object
            login(request,user)
            return redirect('/tweet')
        else:
            template_out = 'login.html'
            logging.info("success: failed")# Return an 'invalid login' error message.
            return redirect('/login')

    #get processed only for the straight gets
    return render_to_response(template_out,{}, context_instance=RequestContext(request))


#create a context to be used in our templates
def user_processor(request):
    return {'username': request.user.username,
            'is_staff': request.user.is_staff}


#the following handles the tweet page with requires the user to be logged in
@login_required(login_url='login')
def tweet(request):   

    if request.method == 'POST':

        user = request.user
        tweet = request.POST['tweet']
        status = request.POST['status']



        tweet = Tweet.create(tweet,user,status)
        tweet.save()


        #if the tweet is clean then tweet it 
        if tweet.status == 'clean':
            #post the tweet to the twitter stream and get back the data we want to store 
            twitterDetails = tweet_handler.postTweet(tweet)

            #instantiate a model object
            tweetDetails = TweetDetails(tweet=tweet, id_str=twitterDetails.id_str, created_at=twitterDetails.created_at, created_at_epoch=twitterDetails.created_at_epoch, retweet_count=twitterDetails.retweet_count, html=twitterDetails.html, stripped_html=twitterDetails.stripped_html)

            #Save the model
            tweetDetails.save();

            data = simplejson.dumps({'tweet_html':twitterDetails.html})


            return HttpResponse(data, mimetype='application/json')



    return render_to_response("tweet.html", context_instance=RequestContext(request,processors=[user_processor]))



#this is typically used to asyncronously get json data
#login is required to access this information. 
@login_required(login_url='login')
def tweets_json(request,current_page=0):   

    if request.method == 'GET':

        try:
            current_page=int(request.GET['page'])
        except:
            pass

        if isstaff(request.user):
            #staff see everything
            tweets = Tweet.objects.all()
        else:
            #other only see their own tweets
            tweets = Tweet.objects.filter(user_id=request.user.id)

        #number of total tweets retreived
        tweets_count = tweets.count()

        #length os frame/page
        page_length = 10

        #get a frame equal to page length
        tweets = tweets[current_page*page_length:(current_page+1)*page_length]

        #logging.info('tweets.users %s' % tweets.users)

        #compute total numer of pages
        total_pages = math.ceil(float(tweets_count)/page_length)


        #I could have used the Django serializer but did not figure out how to format it it to get the data that i wanted
        data = simplejson.dumps({'total':tweets_count, 'total_pages':total_pages,'per_page': page_length, 
                                'page': current_page, 'tweets': [{'username': User.objects.get(id=o.user_id).username, 
                                'id':o.pk, 'tweet': o.tweet,
                                'created_at': o.created_at.strftime("%b %d %Y %H:%M:%S"), 'status':o.status} for o in tweets]})


    return HttpResponse(data, mimetype='application/json')



def isstaff(user):
   return user.is_staff


#The below was used be me to limit tweets_list to staff members
#before I decided to allow non-staff to see their tweet history
#This is minimalistic because backbones handles data to be displayed on the page
#@user_passes_test(isstaff,login_url='login')
@login_required(login_url='login')
def tweets_list(request):   
    template_out = "tweets_list.html"
    return render_to_response(template_out, context_instance=RequestContext(request,processors=[user_processor]))



def checkout(request):
    logout(request)
    return redirect('/login')
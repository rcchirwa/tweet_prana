from django.conf.urls import patterns, include, url
from views import landing, tweet, tweets_json, tweets_list, checkout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',landing),
    url(r'^login/*',landing),
    url(r'^logout/*',checkout),
    url(r'^tweet/*$',tweet),
    url(r'^tweets_json$',tweets_json),
    url(r'^tweets_list$',tweets_list),
    #url(r'^login/$', 'django.contrib.auth.views.login')
    # {'template_name': 'one.html'}),#,name="my_login"),
)

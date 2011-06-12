#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'update/follower$', 'twirem.commander.update.follower'),
	url(r'update/friend$', 'twirem.commander.update.friend'),
	url(r'update/reset$', 'twirem.commander.update.reset'),
)

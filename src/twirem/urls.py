#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('main.urls')),
	url(r'^command', include('commander.urls')),
	url(r'^icons/(?P<digest>[0-9a-fA-F]{40}$)', 'commander.icons.digest'),
    # Examples:
    # url(r'^$', 'twirem.views.home', name='home'),
    # url(r'^twirem/', include('twirem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

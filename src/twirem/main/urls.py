#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^$', 'django.views.generic.simple.direct_to_template', {'template':'main/top.html'}),
	url(r'^$', 'main.views.toppage'),
	url(r'^access_token$', 'main.views.access_token'),
	url(r'^auth$', 'main.views.auth'),
	url(r'^logout$', 'main.views.logout'),
    # Examples:
    # url(r'^$', 'twirem.views.home', name='home'),
    # url(r'^twirem/', include('twirem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

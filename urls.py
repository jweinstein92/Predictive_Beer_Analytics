from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import *

admin.autodiscover()
urlpatterns = patterns('',


                       url(r'^$', listEntries),
                       url(r'^description/', description),
                       url(r'^about/', about),
                       url(r'^map/', map),
                       url(r'^predictions/', prediction),
                       url(r'^getPrediction/', getPrediction),

               )

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


    # Examples:
    # url(r'^$', 'Predictive_Beer_Analytics.views.home', name='home'),
    # url(r'^Predictive_Beer_Analytics/', include('Predictive_Beer_Analytics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


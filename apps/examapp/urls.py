from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.logregpage),
    url(r'^process$', views.process),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.newtrip),
    url(r'^destroy$', views.destroy),
    url(r'^tripcreate$', views.createtrip),
    url(r'^delete/(?P<idnum>\d+)$', views.deltetrip),
    url(r'^trips/edit/(?P<idnum>\d+)$', views.editrip),
    url(r'^edit/(?P<idnum>\d+)$', views.edit),
    url(r'^trips/(?P<idnum>\d+)$', views.tripinfo),
]

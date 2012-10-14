from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'list/$', 'games.views.listgames'),
    url(r'submit/$', 'games.views.submit'),
    url(r'game/(?P<id>\d+)/$', 'games.views.showgame'),

)

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'list/$', 'games.views.listgames'),
    url(r'submitgamebasic/$', 'games.views.submitgamebasic'),
    url(r'game/(?P<id>\d+)/$', 'games.views.showgame'),
    url(r'editgamebasic/(?P<id>\d+)/$', 'games.views.editgamebasic'),
    url(r'editgameplatforms/(?P<id>\d+)/$', 'games.views.editgameplatforms'),
    url(r'editgamecategories/(?P<id>\d+)/$', 'games.views.editgamecategories'),
    url(r'editgamemedia/(?P<id>\d+)/$', 'games.views.editgamemedia'),
    url(r'editgamecontact/(?P<id>\d+)/$', 'games.views.editgamecontact'),

)

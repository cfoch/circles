from django.conf.urls import url

from games.views import GameListView, GameDetailView

urlpatterns = [
    url(r'^$', GameListView.as_view(), name='game-list'),
    url(r'^(?P<pk>\d+)/$', GameDetailView.as_view(), name='game-detail'),
    url(r'^get_payment/$', 'games.views.get_payment'),

]

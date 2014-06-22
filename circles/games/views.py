from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from games.models import Game


class GameListView(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        return context


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        return context

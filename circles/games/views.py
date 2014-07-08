from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# FIXME it is deprecated
from django.utils import simplejson


from games.models import Game
from games.utils import PaymentCalculator


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

@csrf_exempt
@require_POST
def get_payment(request):
    n = request.POST.get('n')
    game_pk = request.POST.get('game')
    calculator = PaymentCalculator(n, game_pk)
    info = {'payment': float(calculator.get_price())}
    data = simplejson.dumps(info)
    return HttpResponse(data, mimetype='application/json')

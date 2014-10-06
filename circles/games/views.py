from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResposneForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# FIXME it is deprecated
from django.utils import simplejson

from games.models import Game
from games.utils import PaymentCalculator, paypal_get_payment_info, paypal_save_payment_info
from circles.settings import PAYPAL_PDT_ID_TOKEN


class GameListView(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        return context

class GameDetailView(DetailView):
    model = Game

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GameDetailView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print request.POST
        return HttpResponse('This is POST request')

    def get(self, request, *args, **kwargs):
        sucess, info = paypal_get_payment_info(request.GET.get("tx"),
            PAYPAL_PDT_ID_TOKEN)
        if sucess:
            if paypal_save_payment_info(info):
                context = self.get_context_data(**kwargs)
                return render_to_response('game_paid.html', context,
                    content_type="application/xhtml+xml")
        return HttpResonseForbidden()


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
    print(n, info)
    return HttpResponse(data, mimetype='application/json')

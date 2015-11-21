from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

import json

from games.models import Game, Payment
from games.utils import PaymentCalculator, paypal_get_payment_info, paypal_save_payment_info
from circles.settings import PAYPAL_PDT_ID_TOKEN


class GameListView(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        return context

class GameDetailView(DetailView):
    model = Game

    def __init__(self, *args, **kwargs):
        super(GameDetailView, self).__init__(*args, **kwargs)
        self.is_paid_game = False
        self.payment = None

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GameDetailView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponse('This is POST request')
    """
    def get(self, request, *args, **kwargs):
<<<<<<< Updated upstream
        tx = request.GET.get("tx")
        if tx:
            sucess, info = paypal_get_payment_info(tx, PAYPAL_PDT_ID_TOKEN)
            if sucess:
                print("success-tx", sucess)
                if paypal_save_payment_info(info):
                    print("MIERDA")
                    context = self.get_context_data(**kwargs)
                    return render_to_response('paid_game.html', context,
                        content_type="application/xhtml+xml")
        #return HttpResponseForbidden()
        return super(GameDetailView, self).get(request, *args, **kwargs)
=======
        sucess, info = paypal_get_payment_info(request.GET.get("tx"),
            PAYPAL_PDT_ID_TOKEN)
        if sucess:
            if paypal_save_payment_info(info):
                context = self.get_context_data(**kwargs)
                return render_to_response('game_paid.html', context,
                    content_type="application/xhtml+xml")
        return HttpResponseForbidden()
    """

    def get_paid_game(self, request, *args, **kwargs):
        # if not self.payment:
        #     TODO: return error
        return super(GameDetailView, self).get(request, *args, **kwargs)

    def get_game(self, request, *args, **kwargs):
        return super(GameDetailView, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if "payment_pk" in kwargs.keys():
            self.is_paid_game = True
            self.payment = Payment.objects.get(pk=kwargs["payment_pk"])
            return self.get_paid_game(request, *args, **kwargs)
        return self.get_game(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context["is_paid_game"] = self.is_paid_game
        context["payment"] = self.payment
        print(context)
        return context


@csrf_exempt
@require_POST
def get_payment(request):
    n = request.POST.get('n')
    game_pk = request.POST.get('game')
    calculator = PaymentCalculator(n, game_pk)
    info = {'payment': float(calculator.get_price())}
    data = json.dumps(info)
    return HttpResponse(data, content_type="application/json")

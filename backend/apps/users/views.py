from django.http import JsonResponse


def home(request):
    return JsonResponse({
        'message': 'Bienvenido a Sec-0,1-bet API',
        'status': 'ok',
    })

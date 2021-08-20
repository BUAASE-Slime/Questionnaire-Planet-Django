from django.shortcuts import render

# Create your views here.
from .form import *
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def all_submittion_count(request):
    if request.method == 'POST':
        try:
            count = int(Submit.objects.all().count())
        except :
            return JsonResponse({'status_code': 1,})
        return JsonResponse({'status_code': 1, 'count': count})
    else:
        return JsonResponse({'status_code': 0, 'count': 0,})

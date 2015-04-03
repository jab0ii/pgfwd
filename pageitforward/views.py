from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    return render(request, 'pageitforward/index.html')




def postLogin(request):
    return render(request, 'pageitforward/postLogin.html')

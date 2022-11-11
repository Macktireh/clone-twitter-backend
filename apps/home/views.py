from django.shortcuts import render


def home(request):
    template = 'home/home.html'
    cntx = {
        "activePage": "home"
    }
    return render(request, template, cntx)
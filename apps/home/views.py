from django.shortcuts import render


def home(request):
    template = 'home/index.html'
    cntx = {}
    return render(request, template, cntx)
from django.shortcuts import render

home_page = None


def home_page(req):
    return render(req, 'home.html')

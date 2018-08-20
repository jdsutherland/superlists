from django.http import HttpResponse
from django.shortcuts import render

home_page = None


def home_page(req):
    return render(req, 'home.html', {
        'new_item_text': req.POST.get('item_text', ''),
    })

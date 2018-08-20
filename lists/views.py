from lists.models import Item
from django.shortcuts import render, redirect

home_page = None


def home_page(req):
    if req.method == 'POST':
        Item.objects.create(text=req.POST['item_text'])
        return redirect('/lists/the-only-list/')

    return render(req, 'home.html')


def view_list(req):
    items = Item.objects.all()
    return render(req, 'list.html', {'items': items})

from lists.models import Item, List
from django.shortcuts import render, redirect

home_page = None


def home_page(req):
    return render(req, 'home.html')


def view_list(req):
    items = Item.objects.all()
    return render(req, 'list.html', {'items': items})


def new_list(req):
    list_ = List.objects.create()
    Item.objects.create(text=req.POST['item_text'],
                        list=list_)
    return redirect('/lists/the-only-list/')

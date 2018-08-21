from django.shortcuts import redirect, render

from lists.models import Item, List

home_page = None


def home_page(req):
    return render(req, 'home.html')


def new_list(req):
    list_ = List.objects.create()
    Item.objects.create(text=req.POST['item_text'],
                        list=list_)
    return redirect(f'/lists/{list_.id}/')


def view_list(req, list_id):
    list_ = List.objects.get(id=list_id)
    return render(req, 'list.html', {'list': list_})


def add_item(req, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=req.POST['item_text'],
                        list=list_)
    return redirect(f'/lists/{list_.id}/')

from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List

home_page = None


def home_page(req):
    return render(req, 'home.html')


def new_list(req):
    list_ = List.objects.create()
    item = Item.objects.create(text=req.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError as e:
        list_.delete()
        return render(req, 'home.html', {'error': e})
    return redirect(f'/lists/{list_.id}/')


def view_list(req, list_id):
    list_ = List.objects.get(id=list_id)

    if req.method == 'POST':
        list_ = List.objects.get(id=list_id)
        Item.objects.create(text=req.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')

    return render(req, 'list.html', {'list': list_})

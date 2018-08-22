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
    except ValidationError:
        list_.delete()
        error = "This field cannot be blank."
        return render(req, 'home.html', {'error': error})
    return redirect(list_)


def view_list(req, list_id):
    error = None
    list_ = List.objects.get(id=list_id)

    if req.method == 'POST':
        try:
            item = Item(text=req.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError as e:
            error = "This field cannot be blank."

    return render(req, 'list.html', {'list': list_, 'error': error})

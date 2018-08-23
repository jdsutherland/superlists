from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List

home_page = None


def home_page(req):
    return render(req, 'home.html', {'form': ItemForm()})


def new_list(req):
    form = ItemForm(data=req.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(req, 'home.html', {'form': form})


def view_list(req, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if req.method == 'POST':
        form = ItemForm(data=req.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(req, 'list.html', {'list': list_, 'form': form})

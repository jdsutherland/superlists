from django.shortcuts import redirect, render

from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List
from django.contrib.auth import get_user_model
User = get_user_model()

home_page = None


def home_page(req):
    return render(req, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def view_list(req, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if req.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=req.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(req, 'list.html', {'list': list_, 'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['sharee'])
    return redirect(list_)

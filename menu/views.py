from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import *


def menu_list(request):
    ''' List all the non expired menus'''
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.filter(expiration_date__gte=timezone.now()
                             ).order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    '''View showing details of each menu'''
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    ''' item details'''
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    '''form to create a new menu when logged in'''
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    '''form to edit an existing menu'''
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})

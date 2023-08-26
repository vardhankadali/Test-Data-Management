from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def supplier_home(request):
    # supplier = get_object_or_404(Supplier, admin=request.user)
    context = {
        'page_title': 'Supplier Homepage'

    }
    return render(request, 'supplier_template/home_content.html', context)


def supplier_view_profile(request):
    supplier = get_object_or_404(Supplier, admin=request.user)
    form = SupplierEditForm(request.POST or None, request.FILES or None,
                           instance=supplier)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                admin = supplier.admin
                if password != None:
                    admin.set_password(password)
                admin.first_name = first_name
                admin.last_name = last_name
                admin.gender = gender
                admin.save()
                supplier.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('supplier_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "supplier_template/supplier_view_profile.html", context)

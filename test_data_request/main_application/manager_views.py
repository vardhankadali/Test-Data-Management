import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def manager_home(request):
    total_requester = Requester.objects.all().count()
    total_suppliers = Supplier.objects.all().count()
    total_managers = Manager.objects.all().count()
    total_requests = Request.objects.all().count()
    new_requests = Request.objects.filter(status="new").count()
    pending_requests = Request.objects.filter(status="pending").count()
    closed_requests = Request.objects.filter(status="closed").count()

    context = {
        'page_title': "Manager Dashboard",
        'total_suppliers': total_suppliers,
        'total_requester': total_requester,
        'total_managers': total_managers,
        'total_requests': total_requests,
        'new_requests': new_requests,
        'pending_requests': pending_requests,
        'closed_requests': closed_requests,

    }
    return render(request, 'manager_template/home_content.html', context)


def manager_view_profile(request):
    manager = get_object_or_404(Manager, admin=request.user)
    form = ManagerEditForm(request.POST or None, request.FILES or None,instance=manager)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                gender = form.cleaned_data.get('gender')
                admin = manager.admin
                if password != None:
                    admin.set_password(password)
                admin.first_name = first_name
                admin.last_name = last_name
                admin.gender = gender
                admin.save()
                manager.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('manager_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "manager_template/manager_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "manager_template/manager_view_profile.html", context)

    return render(request, "manager_template/manager_view_profile.html", context)

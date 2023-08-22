import json
from django.forms.models import BaseModelForm
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def admin_home(request):
    total_requester = Requester.objects.all().count()
    total_suppliers = Supplier.objects.all().count()
    
    supplier_name_list=[]

    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        supplier_name_list.append(supplier.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_suppliers': total_suppliers,
        'total_requester': total_requester,
        "supplier_name_list": supplier_name_list,

    }
    return render(request, 'admin_template/home_content.html', context)


def add_requester(request):
    form = RequesterForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Requester'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.requester.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_requester'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'admin_template/add_requester_template.html', context)


def add_supplier(request):
    supplier_form = SupplierForm(request.POST or None, request.FILES or None)
    context = {'form': supplier_form, 'page_title': 'Add Supplier'}
    if request.method == 'POST':
        if supplier_form.is_valid():
            first_name = supplier_form.cleaned_data.get('first_name')
            last_name = supplier_form.cleaned_data.get('last_name')
            address = supplier_form.cleaned_data.get('address')
            email = supplier_form.cleaned_data.get('email')
            gender = supplier_form.cleaned_data.get('gender')
            password = supplier_form.cleaned_data.get('password')
            course = supplier_form.cleaned_data.get('course')
            session = supplier_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.supplier.session = session
                user.supplier.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_supplier'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'admin_template/add_supplier_template.html', context)



def manage_requester(request):
    allRequester = CustomUser.objects.filter(user_type=2)
    context = {
        'allRequester': allRequester,
        'page_title': 'Manage Requester'
    }
    return render(request, "admin_template/manage_requester.html", context)


def manage_supplier(request):
    suppliers = CustomUser.objects.filter(user_type=3)
    context = {
        'suppliers': suppliers,
        'page_title': 'Manage Suppliers'
    }
    return render(request, "admin_template/manage_supplier.html", context)



def edit_requester(request, requester_id):
    requester = get_object_or_404(Requester, id=requester_id)
    form = RequesterForm(request.POST or None, instance=requester)
    context = {
        'form': form,
        'requester_id': requester_id,
        'page_title': 'Edit Requester'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=requester.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                requester.course = course
                user.save()
                requester.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_requester', args=[requester_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=requester_id)
        requester = Requester.objects.get(id=user.id)
        return render(request, "admin_template/edit_requester_template.html", context)


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    form = SupplierForm(request.POST or None, instance=supplier)
    context = {
        'form': form,
        'supplier_id': supplier_id,
        'page_title': 'Edit Supplier'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=supplier.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                supplier.session = session
                user.gender = gender
                user.address = address
                supplier.course = course
                user.save()
                supplier.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_supplier', args=[supplier_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin_template/edit_supplier_template.html", context)



@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "admin_template/admin_view_profile.html", context)






def delete_requester(request, requester_id):
    requester = get_object_or_404(CustomUser, requester__id=requester_id)
    requester.delete()
    messages.success(request, "Requester deleted successfully!")
    return redirect(reverse('manage_requester'))


def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(CustomUser, supplier__id=supplier_id)
    supplier.delete()
    messages.success(request, "Supplier deleted successfully!")
    return redirect(reverse('manage_supplier'))

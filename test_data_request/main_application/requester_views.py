import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def requester_home(request):
    # requester = get_object_or_404(Requester, admin=request.user)
    context = {
        'page_title': 'Requester Panel',
    }
    return render(request, 'requester_template/home_content.html', context)


def requester_view_profile(request):
    requester = get_object_or_404(Requester, admin=request.user)
    form = RequesterEditForm(request.POST or None, request.FILES or None,instance=requester)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = requester.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.gender = gender
                admin.save()
                requester.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('requester_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "requester_template/requester_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "requester_template/requester_view_profile.html", context)

    return render(request, "requester_template/requester_view_profile.html", context)

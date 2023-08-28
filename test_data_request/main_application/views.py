import json
from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .mail_backend import EmailBackend
from .forms import *
from .models import *
from .filters import *


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("requester_home"))
        elif request.user.user_type == '3':
            return redirect(reverse("supplier_home"))
        elif request.user.user_type == '4':
            return redirect(reverse("manager_home"))
    return render(request, 'main_application/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:

        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_key = "6LfswtgZAAAAABX9gbLqe-d97qE2g1JP8oUYritJ"
        data = {
            'secret': captcha_key,
            'response': captcha_token
        }

        try:
            captcha_server = requests.post(url=captcha_url, data=data)
            response = json.loads(captcha_server.text)
            if response['success'] == False:
                messages.error(request, 'Invalid Captcha. Try Again')
                return redirect('/')
        except:
            messages.error(request, 'Captcha could not be verified. Try Again')
            return redirect('/')

        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("requester_home"))
            elif user.user_type == '3':
                return redirect(reverse("supplier_home"))
            elif user.user_type == '4':
                return redirect(reverse("manager_home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")



class RequestListView(ListView):
    model = Request
    template_name = "main_application/view_requests.html"
    context_object_name = "requests"
    # ordering = ['-date_posted']

    def get_queryset(self):
        if 'new' in self.request.GET:
            return Request.objects.filter(status="new").order_by('-date_posted')
        elif 'pending' in self.request.GET:
            return Request.objects.filter(status="pending").order_by('-date_posted')
        elif 'closed' in self.request.GET:
            return Request.objects.filter(status="closed").order_by('-date_posted')
        else:
            return Request.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "View Requests"
        context["filter"] = RequestFilter(self.request.GET, queryset=self.get_queryset())
        return context


class RequestListViewReq(ListView):
    model = Request
    template_name = "main_application/view_requests.html"
    context_object_name = "requests"
    # ordering = ['-date_posted']
    def get_queryset(self):
        return Request.objects.filter(requested_by=self.request.user).order_by('-date_posted')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "My Requests"
        return context


class RequestListViewAs(ListView):
    model = Request
    template_name = "main_application/view_requests.html"
    context_object_name = "requests"
    # ordering = ['-date_posted']
    def get_queryset(self):
        o = self.request.user
        return Request.objects.filter(assigned_to=o.first_name + " " + o.last_name).order_by('-date_posted')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Assigned Requests"
        return context


class RequestDetailView(DetailView):
    model = Request
    template_name = "main_application/detail_view.html"
    context_object_name = "requests"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "View Request"
        return context


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RaiseRequestForm
    template_name = "main_application/create_requests.html"
    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        return super().form_valid(form)
    def get_form(self):
        form = super().get_form()
        form.fields["expected_date"].widget = DatePickerInput()
        return form


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    form_class = UpdateRequestForm
    template_name = "main_application/update_requests.html"
    context_object_name = "requests"

def download(request, request_id):
    document = get_object_or_404(Request, pk=request_id)
    response = HttpResponse(document.document, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
    return response


def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")
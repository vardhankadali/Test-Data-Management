import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .mail_backend import EmailBackend
from .forms import *
from .models import *
# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("requester_home"))
        elif request.user.user_type == '3':
            return redirect(reverse("supplier_home"))
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
        else:
            messages.error(request, "Invalid details")
            return redirect("/")



class RequestListView(ListView):
    model = Request
    template_name = "main_application/view_requests.html"
    context_object_name = "requests"
    ordering = ['-date_posted']



class RequestListViewReq(ListView):
    model = Request
    template_name = "main_application/view_requests.html"
    context_object_name = "requests"
    ordering = ['-date_posted']
    def get_queryset(self):
        return Request.objects.filter(requested_by=self.request.user)



class RequestDetailView(DetailView):
    model = Request
    template_name = "main_application/detail_view.html"
    context_object_name = "requests"


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    fields = ["status", "requested_by", "type_of_request", "env_swimlane",
               "project_name", "number_of_records", "application", "expected_date", "type_of_data_setup",
               "stakeholders", "state_jurisdiction", "synopsis_of_request", "description_of_request"]
    template_name = "main_application/create_requests.html"
    def get_form(self):
        form = super().get_form()
        form.fields["expected_date"].widget = DatePickerInput()
        return form


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    fields = ["status","test_data"]
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
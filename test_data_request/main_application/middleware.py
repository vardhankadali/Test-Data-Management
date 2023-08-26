from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == 'main_application.supplier_views' or modulename == 'main_application.requester_views' or modulename == 'main_application.manager_views':
                    return redirect(reverse('admin_home'))
            elif user.user_type == '2':
                if modulename == 'main_application.supplier_views' or modulename == 'main_application.admin_views' or modulename == 'main_application.manager_views':
                    return redirect(reverse('requester_home'))
            elif user.user_type == '3':
                if modulename == 'main_application.admin_views' or modulename == 'main_application.requester_views' or modulename == 'main_application.manager_views':
                    return redirect(reverse('supplier_home'))
            elif user.user_type == '4':
                if modulename == 'main_application.admin_views' or modulename == 'main_application.requester_views' or modulename == 'main_application.supplier_views':
                    return redirect(reverse('manager_home'))
            else:
                return redirect(reverse('login_page'))
        else:
            if request.path == reverse('login_page') or modulename == 'django.contrib.auth.views' or request.path == reverse('user_login'):
                pass
            else:
                return redirect(reverse('login_page'))

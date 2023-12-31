from django.urls import path, re_path

from . import admin_views, requester_views, supplier_views, manager_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("requester/add", admin_views.add_requester, name='add_requester'),
    path("admin_view_profile", admin_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", admin_views.check_email_availability,
         name="check_email_availability"),
    path("supplier/add/", admin_views.add_supplier, name='add_supplier'),
    path("manager/add/", admin_views.add_manager, name='add_manager'),
    path("requester/manage/", admin_views.manage_requester, name='manage_requester'),
    path("supplier/manage/", admin_views.manage_supplier, name='manage_supplier'),
    path("manager/manage/", admin_views.manage_manager, name='manage_manager'),
    path("requester/edit/<int:requester_id>", admin_views.edit_requester, name='edit_requester'),
    path("requester/delete/<int:requester_id>",admin_views.delete_requester, name='delete_requester'),
    path("supplier/delete/<int:supplier_id>",admin_views.delete_supplier, name='delete_supplier'),
    path("supplier/edit/<int:supplier_id>",admin_views.edit_supplier, name='edit_supplier'),
    path("manager/delete/<int:manager_id>",admin_views.delete_manager, name='delete_manager'),
    path("manager/edit/<int:manager_id>",admin_views.edit_manager, name='edit_manager'),

    re_path(r"^requests/all$", views.RequestListView.as_view(), name='view_requests_all'),
    path("supplier/requests/", views.RequestListViewAs.as_view(), name='view_requests_as'),
    path("requester/requests/", views.RequestListViewReq.as_view(), name='view_requests_req'),
    path("requests/new/", views.RequestCreateView.as_view(), name='create_requests'),
    path("requests/<int:pk>/", views.RequestDetailView.as_view(), name='detail_requests'),
    path("requests/<int:pk>/update", views.RequestUpdateView.as_view(), name='update_requests'),
    
    path("requester/home/", requester_views.requester_home, name='requester_home'),
    path("requester/view/profile/", requester_views.requester_view_profile,
         name='requester_view_profile'),

    path("supplier/home/", supplier_views.supplier_home, name='supplier_home'),
    path("supplier/view/profile/", supplier_views.supplier_view_profile,
         name='supplier_view_profile'),
     
    path("manager/home/", manager_views.manager_home, name='manager_home'),
    path("manager/view/profile/", manager_views.manager_view_profile,
         name='manager_view_profile'),

]

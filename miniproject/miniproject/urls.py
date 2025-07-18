
from django.contrib import admin
from django.urls import path
from myapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    ###User Path###
    path('admin/', admin.site.urls),
    path('', views.guest_page),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'), 
    path('user_home_login', views.user_home_login, name='user_home_login'),
    path('register_complaint', views.register_complaint, name='register_complaint'),
    path('success', views.success, name='success'),
    path('view_complaint', views.view_complaint, name='view_complaint'),
    path('admin_complainte',views.admin_complainte,name='admin_complainte'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),

    ###Admin Path###
    path('feedback_view', views.feedback_view, name='feedback_view'),
    path('admin_feedback', views.admin_feedback, name='admin_feedback'),
    path('feedback/toggle/<int:feedback_id>/', views.toggle_feedback, name='toggle_visibility'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('delete_user',views.delete_user, name='delete_user'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('accounts/login/', views.sign_in, name='login'),
    path('admin-complaints/update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('admin-complaint/delete/<int:complaint_id>/',views.delete_complaint,name='delete_complaint'),

    ###Contact info###
    path('contact_view',views.contact_view,name='contact_view'),
    path('about_view',views.about_view,name='about_view'),

    path('admin_users_list', views.users_list_view, name='admin_users_list'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
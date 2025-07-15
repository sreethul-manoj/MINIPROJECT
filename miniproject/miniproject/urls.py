"""
URL configuration for miniproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.guest_page),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'), 
    path('user_home_login', views.user_home_login, name='user_home_login'),
    path('register_complaint', views.register_complaint, name='register_complaint'),
    path('success', views.success, name='success'),
    path('view_complaint', views.view_complaint, name='view_complaint'),
    path('admin_complaint',views.admin_complainte,name='admin_complainte'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),

    
    path('feedback_view', views.feedback_view, name='feedback_view'),
    path('feedback-admin', views.admin_feedback, name='admin_feedback'),
    path('feedback/toggle/<int:feedback_id>/', views.toggle_feedback, name='toggle_visibility'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('delete_user',views.delete_user, name='delete_user'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('accounts/login/', views.sign_in, name='login'),

    path('contact_view',views.contact_view,name='contact_view'),
    path('about_view',views.about_view,name='about_view'),

    path('admin_user_list', views.admin_user_list, name='admin_user_list'),

    
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
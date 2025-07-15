from django.contrib import admin
from .models import Feedback, Complaint, Signup

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'mobile_number', 'date_of_birth')
    search_fields = ('fullname', 'email', 'mobile_number')
    list_filter = ('date_of_birth',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'complaint_type', 'location', 'submitted_at', 'verified')
    search_fields = ('user__email', 'complaint_type', 'location')
    list_filter = ('complaint_type', 'verified', 'submitted_at')
    readonly_fields = ('submitted_at',)


# admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_at', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('name', 'suggestion')

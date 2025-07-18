from django.shortcuts import render, redirect,get_object_or_404
from .models import Signup, Complaint ,Feedback
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

#Guest Home

def guest_page(request):
    return render(request, 'user_home_guest.html')


#User Home After Login

def user_home_login(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user_email = request.session.get('user_email')
    user_complaint_count = Complaint.objects.filter(user_id=user_id).count()

    context = {
        'user_email': user_email,
        'user_complaint_count': user_complaint_count
    }
    return render(request, 'user_home_login.html', context)


#Sign Up

def sign_up(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('sign_up')

        Signup.objects.create(
            fullname=fullname,
            mobile_number=mobile_number,
            date_of_birth=date_of_birth,
            email=email,
            password=make_password(password)
        )
        messages.success(request, "Sign-up successful! Please log in.")
        return redirect('sign_in')

    return render(request, 'sign_up.html')


#Sign In

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'admin@123' and password == 'admin':
            request.session['user_email'] = 'admin'
            request.session['is_admin'] = True
            return render(request, 'admin_dashboard.html')

        try:
            user = Signup.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['is_admin'] = False
                return redirect('user_home_login')
            else:
                messages.error(request, "Incorrect password.")
        except Signup.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'sign_in.html')

# Sign Out

def sign_out(request):
    request.session.flush()
    return redirect('sign_in')


#Register Complaint

def register_complaint(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    if request.method == 'POST':
        user = get_object_or_404(Signup, id=user_id)
        description = request.POST.get('description')
        complaint_type = request.POST.get('complaint_type')  
        location = request.POST.get('location')
        proof = request.FILES.get('proof')

        Complaint.objects.create(
            user=user,
            description=description,
            complaint_type=complaint_type,
            location=location,
            proof=proof
        )
        return redirect('success')

    return render(request, 'register_complaint.html')


# View Complaints

def view_complaint(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user = Signup.objects.get(id=user_id)
    complaints = Complaint.objects.filter(user=user).order_by('-submitted_at')
    return render(request, 'view_complaint.html', {'complaints': complaints})


# Success Page 

def success(request):
    return render(request, 'success.html')


############### Admin Dashboard#####################

# Admin Dashboard

def admin_dashboard(request):
    total = Complaint.objects.count()
    pending=Complaint.objects.filter(status='pending').count()
    resolved=Complaint.objects.filter(status='resolved').count()
    in_progress=Complaint.objects.filter(status='in_progress').count()
    status={
        'total_complaints': total,
        'pending_complaints': pending,
        'resolved_complaints': resolved,
        'in_progress_complaints': in_progress,
    }      
    
    return render(request, 'admin_dashboard.html',status)


# Admin Complaints View

def admin_complainte(request):
    complaints = Complaint.objects.all().order_by('-submitted_at')
    return render(request, 'admin_complainte.html', {'complaints': complaints})


#update complaints

def update_status(request, complaint_id):

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.save()

    return redirect('admin_complainte')



#delete Complaint

def delete_complaint(request,complaint_id):
    if request.method == "POST":
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
    return redirect('admin_complainte')


##########feed back###########

# User Feedback Submission + View

def feedback_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        suggestion = request.POST.get('suggestion')

        if name and suggestion:
            Feedback.objects.create(name=name, suggestion=suggestion, is_visible=True)
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback_view')

    feedback_list = Feedback.objects.filter(is_visible=True).order_by('-submitted_at')
    paginator = Paginator(feedback_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feedback.html', {'page_obj': page_obj})


# Admin View for All Feedback

def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'feedback_admin.html', {'feedbacks': feedback_list})


# Admin Toggle Visibility

def toggle_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.is_visible = not feedback.is_visible
        feedback.save()
    return redirect('admin_feedback')


# Admin Delete Feedback

def delete_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
    return redirect('admin_feedback')


# Delete User

def delete_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_home_login')

    try:
        user = Signup.objects.get(id=user_id)
        user.delete()
        request.session.flush()
        messages.success(request, "User deleted successfully.")
        return redirect('guest_page')
    except Signup.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_home_login')


#Edit Profile

def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user = Signup.objects.get(id=user_id)

    if request.method == 'POST':
        user.fullname = request.POST.get('fullname')
        user.mobile_number = request.POST.get('mobile_number')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user_home_login')

    return render(request, 'user_profile.html', {'user': user})


#contact info

def contact_view(request):
    return render(request, 'contact.html')

#About
def about_view(request):
    return render(request,'about.html')

# All Users list

def users_list_view(request):
    users = Signup.objects.all()
    return render(request, 'admin_userlist.html', {'users': users})

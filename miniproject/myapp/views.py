from django.shortcuts import render, redirect,get_object_or_404
from .models import Signup, Complaint
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Feedback

# ------------------ Guest Home ------------------
def guest_page(request):
    return render(request, 'user_home_guest.html')

# ------------------ User Home After Login ------------------
def user_home_login(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user_email = request.session.get('user_email')

    # Count only complaints submitted by this user
    user_complaint_count = Complaint.objects.filter(user_id=user_id).count()

    context = {
        'user_email': user_email,
        'user_complaint_count': user_complaint_count
    }
    return render(request, 'user_home_login.html', context)

# ------------------ Sign Up ------------------
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

# ------------------ Sign In ------------------
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ Admin hardcoded login
        if email == 'admin@123' and password == 'admin':
            request.session['user_email'] = 'admin'
            request.session['is_admin'] = True
            return render(request, 'admin_dashboard.html')

        # ✅ Normal user login
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

# ------------------ Admin Dashboard ------------------
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

#-------Admin_complainte----------

def admin_complainte(request):
    # Fetch all complaints with user information
    complaints = Complaint.objects.select_related('user').all().order_by('-submitted_at')
    return render(request, 'admin_complainte.html', {'complaints': complaints})


# ------------------ Sign Out ------------------
def sign_out(request):
    request.session.flush()
    return redirect('sign_in')

# ------------------ Register Complaint ------------------
def register_complaint(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    if request.method == 'POST':
        user = Signup.objects.get(id=user_id)
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

# ------------------ View Complaints ------------------
def view_complaint(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user = Signup.objects.get(id=user_id)
    complaints = Complaint.objects.filter(user=user).order_by('-submitted_at')
    return render(request, 'view_complaint.html', {'complaints': complaints})

# ------------------ Success Page ------------------
def success(request):
    return render(request, 'success.html')



#feed back

# User Feedback Submission + View
def feedback_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        suggestion = request.POST.get('suggestion')

        if name and suggestion:
            Feedback.objects.create(name=name, suggestion=suggestion, is_visible=True)
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback_view')  # Prevent form resubmission on refresh

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



#user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Allow any logged-in user to see the user list

def admin_user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_userlist.html', {'users': users})





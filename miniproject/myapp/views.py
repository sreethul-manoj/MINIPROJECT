from django.shortcuts import render, redirect
from .models import Signup, Complaint
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login


# guest home
def guest_page(request):
    return render(request, 'user_home_guest.html')

# user home after login
def user_home_login(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')
    context = {'user_email': request.session.get('user_email')}
    return render(request, 'user_home_login.html', context)

# sign up
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

# sign in
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return redirect('user_home_login')
            else:
                messages.error(request, "Incorrect password.")
        except Signup.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'sign_in.html')


# def sign_in(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('user_home_login')  # Redirect to your home/dashboard view
#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'sign_in.html')

# def sign_in(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         print("Email entered:", email)
#         print("Password entered:", password)

#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             print("User authenticated:", user)
#             login(request, user)
#             return redirect('user_home_login')
#         else:
#             print("Authentication failed.")
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'sign_in.html')


# logout
def sign_out(request):
    request.session.flush()
    return redirect('sign_in')

# register complaint
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

# view complaint
def view_complaint(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('sign_in')

    user = Signup.objects.get(id=user_id)
    complaints = Complaint.objects.filter(user=user).order_by('-submitted_at')
    return render(request, 'view_complaint.html', {'complaints': complaints})

# success page
def success(request):
    return render(request, 'success.html')

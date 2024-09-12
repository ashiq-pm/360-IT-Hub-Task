from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from .models import Service
from .forms import ServiceForm, SubscriptionForm
import random
import razorpay

otp_sent = None
temp_user = None

client = razorpay.Client(auth=("rzp_test_e664V0FP0zQy7N", "QdnuRxUHrPGeiJc9lDTXYPO7"))

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username = username):
            messages.error(request, "Username already exists.")
            return redirect('signup')
        
        if User.objects.filter(email = email):
            messages.error(request, "Email already exists.")
            return redirect('signup')

        if password == confirm_password:
            global temp_user
            temp_user = User(username=username, email=email)
            temp_user.set_password(password)
            
            global otp_sent
            otp_sent = random.randint(100000, 999999)
            name = name

            send_mail(
                'Your OTP Code',
                f'Hi {name},\nWelcome to IT Services. \nYour OTP is {otp_sent} .',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return redirect('verify_otp')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

    return render(request, 'signup.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']

        if int(otp) == otp_sent:
            temp_user.save()  
            messages.success(request, 'Your account has been created. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'login.html')

@login_required
def home(request):
    services = Service.objects.filter(active=True, user=request.user).values('id', 'service_name', 'service_price')
    return render(request, 'home.html', {'services': services})

def signout(request):
    logout(request)
    return redirect('login')

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect('service_list')  
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})

@login_required
def service_list(request):
    services = Service.objects.filter(user=request.user)
    return render(request, 'service_list.html', {'services': services})

@login_required
def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'update_service.html', {'form': form})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, user=request.user)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'delete_service.html', {'service': service})

@login_required
def subscription_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    net_price = service.service_price + (service.service_price * service.service_tax / 100)  

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']

            razorpay_order = client.order.create({
                "amount": int(net_price * 100), 
                "currency": "INR",
                "payment_capture": "1"
            })
            order_id = razorpay_order['id']

            return render(request, 'razorpay_payment.html', {
                'service': service,
                'order_id': order_id,
                'net_price': net_price,
                'razorpay_key': "rzp_test_e664V0FP0zQy7N",
                'address': address,
            })
    else:
        form = SubscriptionForm()

    return render(request, 'subscription.html', {'service': service, 'net_price': net_price, 'form': form})

@login_required
def payment_success(request):
    if request.method == "POST":
        payment_data = request.POST
        messages.success(request, "Payment Successful!")
        return redirect('home')
    return render(request, 'payment_success.html')









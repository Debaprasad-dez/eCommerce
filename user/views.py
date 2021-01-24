from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from .forms import *
from .models import *
from order.models import *
from product.models import *

# Create your views here.


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            # userprofile = UserProfile.objects.get(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url

            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(
                request, "Login error!! Username or password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    #category = Category.objects.all()
    context = {  # 'category': category
    }
    return render(request, 'user/login_form.html', context)


@login_required(login_url='/user/login')  # Check login
def index(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {  # 'category': category,
        'profile': profile}
    return render(request, 'user_profile.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

def registerPage(request):
    User = get_user_model()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Signup error!! Invalid email or email already taken")
            else: 
                user = form.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('user/email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, 'expresstotell@gmail.com', [to_email], fail_silently=False,)
                print(send_mail)
                print(to_email)
                print(message)
                return render(request, 'user/confirm_email.html')
            
    context = {'form': form}
    return render(request, 'user/signup_form.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'user/email_confirmed.html')
    else:
        return render(request, 'user/verification_failed.html')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    #category = Category.objects.all()
    context = {  # 'category': category,
        'form': form,
    }
    return render(request, 'user/signup_form.html', context)


@login_required(login_url='/user/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'orders': orders,
               }
    return render(request, 'user/user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_details.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'order_product': order_product,
               }
    return render(request, 'user/user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_detail.html', context)

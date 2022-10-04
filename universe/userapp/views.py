from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm, Profile_form, User_form
from .models import profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import transaction

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def myProfile(request):
    user_details = profile.objects.all().filter(user_id=request.user.id)
    return render(request, 'userapp/myprofile.html', {'userDetails':user_details})    

@login_required
@transaction.atomic
def editMyProfile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        user_form = User_form(request.POST, instance=user)
        profile_form = Profile_form(request.POST or None, request.FILES or None, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            my_details = profile.objects.all().filter(user_id=request.user.id)
            if profile_form.cleaned_data['staff']:
                user.is_staff = True
                my_details.staff = True
                my_details.save()
                user.save()
            else:
                user.is_staff = False
                my_details.staff = False
                my_details.save()
                user.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return myProfile(request)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponseRedirect('edit_profile')
    else:
        user = get_object_or_404(User, id=request.user.id)
        user_form = User_form(instance=user)
        profile_form = Profile_form(instance=user.profile)
        return render(request, 'userapp/user_edit_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form     
        })

@login_required
def updateUserProfile(request, user_id):
    user_details = profile.objects.all().filter(user_id=user_id)
    return render(request, 'userapp/userProfile.html', {'userDetails':user_details})

@login_required
@transaction.atomic
# @permission_required('User.is_staff')
def editUserProfile(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user_form = User_form(request.POST, instance=user)
        profile_form = Profile_form(request.POST or None, request.FILES or None, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            my_details = profile.objects.all().filter(user_id=request.user.id)
            if profile_form.cleaned_data['staff']:
                user.is_staff = True
                my_details.staff = True
                my_details.save()
                user.save()
            else:
                user.is_staff = False
                my_details.staff = False
                my_details.save()
                user.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return updateUserProfile(request, user_id)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponseRedirect('edit_otheruser_profile')
    else:
        user = get_object_or_404(User, id=user_id)
        user_form = User_form(instance=user)
        profile_form = Profile_form(instance=user.profile)
        return render(request, 'userapp/user_edit_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form     
        })


@login_required
def deactivateUser(request, user_id):  
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = 0
    else:
        user.is_active = 1
    user.save()
    return updateUser(request, user_id)

@login_required
def manageStaff(request):
    staff_details = profile.objects.all().filter(staff=True)
    return render(request, 'userapp/manage_staff.html',
    {'staff_details':staff_details})

@login_required
def manageCustomer(request):
    customer_details = profile.objects.all().filter(staff=False)
    return render(request, 'userapp/manage_customer.html',
    {'customer_details':customer_details})
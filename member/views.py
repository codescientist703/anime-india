from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, CreateProfile, PasswordChangingForm
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.views import PasswordChangeView,  PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.urls import reverse_lazy
from .models import Profile
from forum import models
from django.contrib.messages.views import SuccessMessageMixin


class CreateUser(View):
    form_class = CreateUserForm
    template_name = 'auth/register.html'

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            num_results = User.objects.filter(email=email).count()
            if num_results == 0:
                obj = form.save()
                messages.info(
                    request, 'You have been successfully registered.')
                return redirect('login')
            else:
                messages.warning(request, 'Email already exists.')

        return render(request, self.template_name, {'form': form})


class LoginUser(View):
    template_name = 'auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        num_results = User.objects.filter(email=email)
        if num_results.count() == 0:
            messages.warning(request, 'Email is incorrect.')
            return redirect('login')

        username = num_results[0].username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next') != None:
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            messages.warning(request, 'Password is incorrect.')
            return redirect('login')


def logout(request):
    django_logout(request)
    return redirect('home')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class PasswordsChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_change')
    success_message = 'Password was successfully updated'
    template_name = 'auth/change_password.html'


class PasswordsResetView(SuccessMessageMixin, PasswordResetView):
    success_url = reverse_lazy('password_reset')
    success_message = 'Email has been sent to reset the password'
    template_name = 'auth/reset_password.html'


class PasswordsResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_done')
    template_name = 'auth/confirm_password.html'


def passwordResetDone(request):
    return render(request, 'auth/reset_done.html')


def profile(request, username):
    userId = get_object_or_404(User, username=username).id
    myProfile = get_object_or_404(Profile, user=userId)

    recentTopics = models.Topic.objects.filter(user=userId)[:10]
    recentReplies = models.Reply.objects.filter(
        user=userId).order_by('-published_date')[:10]

    topicCount = models.Topic.objects.filter(user=userId).count()
    replyCount = models.Reply.objects.filter(user=userId).count()
    context = {
        'profile': myProfile,
        'recent': recentTopics,
        'replies': recentReplies,
        'topicCount': topicCount,
        'replyCount': replyCount

    }
    return render(request, 'profile/profile.html', context)


@login_required(login_url='/login')
def createProfile(request):
    profile = request.user.profile
    form = CreateProfile(instance=profile)
    if request.method == 'POST':
        form = CreateProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'profile/profile_update.html', context)


def testView(request):
    return render(request, '403.html')

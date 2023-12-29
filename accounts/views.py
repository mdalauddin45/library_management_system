from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.template.loader import render_to_string
from django.views.generic import ListView
from book.models import Purchase
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    balance = 0 

    def get(self, request):
        user_purchases = Purchase.objects.filter(user=request.user)
        account_balance = request.user.account.balance

        return render(request, self.template_name, {
            'user_purchases': user_purchases,
            'account_balance': account_balance,
        })

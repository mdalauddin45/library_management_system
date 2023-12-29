from django.shortcuts import render
from transactions.models import Transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from .forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{
        'user': user,
        'amount':amount,
    })
    send_email = EmailMultiAlternatives(subject, '',to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title': self.title
        })
        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=['balance'])
        
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user,amount,"Deposit Message", 'transactions/deposit_email.html' )
        return super().form_valid(form)

class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context

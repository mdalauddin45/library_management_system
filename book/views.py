from typing import Any
from .import forms
from django.shortcuts import redirect
from .import models
from django.views.generic import DetailView
from .models import Book
from django.contrib import messages
from book.models import Purchase
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm


# Create your views here.

class DetailsPostView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()

        comment_form = ReviewForm(request.POST, book=post, user=request.user)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your review has been added successfully!')
            return self.get(request, *args, **kwargs)
        else:
            if not Purchase.objects.filter(user=request.user, book=post).exists():
                messages.error(request, 'Can not added your review , if you can give this book review must be purchased it bro')
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.comments.all()
        review_form= forms.ReviewForm()
            
        context['reviews']= reviews
        context['review_form']= review_form
        return context

class PurchaseView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)

        if request.user.account.balance < book.price:
            messages.error(request, "Insufficient balance to make the purchase.")
        else:
            purchase = Purchase.objects.create(user=request.user, book=book)
            request.user.account.balance -= book.price
            request.user.account.save()

            messages.success(request, "Purchase successful. Balance deducted.")

        return redirect('profile')
        


           
from typing import Any
from .import forms
from django.shortcuts import redirect
from .import models
from django.views.generic import DetailView
from .models import Book
from django.contrib import messages
from book.models import Purchase
from django.contrib.auth.decorators import login_required


# Create your views here.

class DetailsPostView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form= forms.ReviewForm()
            
        context['comments']= comments
        context['comment_form']= comment_form
        return context

@login_required
def purchase(request,id):
    book = Book.objects.get(id=id)
    purchase = Purchase.objects.create(user=request.user, book=book)      
    messages.success(request, "Buy successfully")
    return redirect('profile')
        


           
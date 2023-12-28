from django import forms
from .models import Book, UserReviews

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['author']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReviews
        fields = ['name','email','body']
        
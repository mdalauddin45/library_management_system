from django.contrib import admin
from django.urls import path,include
from core.views import HomeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('home/<slug:category_slug>/', HomeView.as_view(), name='category_wise_post'),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('books/', include('book.urls')),
] 

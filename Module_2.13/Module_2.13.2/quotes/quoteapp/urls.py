from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('author_detail/<str:author_name>',
         views.author_detail, name='author_detail'),
    path('quote/', views.quote, name='quote'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
]

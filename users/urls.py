from django.http.response import HttpResponse
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
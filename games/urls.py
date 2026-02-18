from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('list/', views.GameListView.as_view(), name='game-list'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('create/', views.GameCreateView.as_view(), name='game-create'),
    path('update/<int:pk>/', views.GameUpdateView.as_view(), name='game-update'),
    path('delete/<int:pk>/', views.GameDeleteView.as_view(), name='game-delete'),
]
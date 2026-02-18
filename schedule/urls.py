from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('list/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
    path('create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('update/<int:pk>/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('delete/<int:pk>/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
]
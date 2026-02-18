from django.urls import path, include
from . import views

app_name = 'groups'

squadsurls = [
    path('list/', views.SquadListView.as_view(), name='squad-list'),
    path('<int:pk>/', views.SquadDetailView.as_view(), name='squad-detail'),
    path('create/', views.SquadCreateView.as_view(), name='squad-create'),
    path('update/<int:pk>/', views.SquadUpdateView.as_view(), name='squad-update'),
    path('delete/<int:pk>/', views.SquadDeleteView.as_view(), name='squad-delete'),
]

eventsurls = [
    path('list/', views.EventListView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='event-update'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name='event-delete'),
]

urlpatterns = [
    path('squads/', include(squadsurls)),
    path('events/', include(eventsurls)),
]
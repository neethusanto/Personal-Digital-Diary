from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('entry/create/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<str:entry_id>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entry/<str:entry_id>/edit/', views.EntryEditView.as_view(), name='entry_edit'),
    path('entry/<str:entry_id>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/<str:entry_id>/export/', views.EntryExportView.as_view(), name='entry_export'),
]


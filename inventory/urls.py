from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<str:item_id>/', views.edit, name='edit'),
    path('write-off/<str:item_id>/', views.write_off, name='write_off'),
    path('delete/<str:item_id>/', views.delete, name='delete'),
    path('change-status/<str:item_id>/', views.change_status, name='change_status')
]
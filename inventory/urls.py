from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Inventory Management
    path('inventory/', views.InventoryItemListView.as_view(), name='inventory_list'),
    path('inventory/add/', views.AddItem.as_view(), name='add_item'),
    path('inventory/<int:pk>/edit/', views.EditItem.as_view(), name='edit_item'),
    path('inventory/<int:pk>/delete/', views.DeleteItem.as_view(), name='delete_item'),
    path('inventory/usage/', views.RecordUsage.as_view(), name='record_usage'),
    
    # Room Management
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/add/', views.AddRoom.as_view(), name='add_room'),
    path('rooms/<int:pk>/edit/', views.EditRoom.as_view(), name='edit_room'),
    
    # Housekeeping
    path('tasks/', views.HousekeepingTaskListView.as_view(), name='task_list'),
    path('tasks/add/', views.AddTask.as_view(), name='add_task'),
    path('tasks/<int:pk>/edit/', views.UpdateTask.as_view(), name='update_task'),
    
    # Reports
    path('reports/', views.ReportsView.as_view(), name='reports'),
]
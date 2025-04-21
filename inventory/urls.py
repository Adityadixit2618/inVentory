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
    path('logout/', views.logout_view, name='logout'),
    
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

    path('products/', views.product_list, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    path('orders/', views.order_list, name='orders'),
    path('orders/add/', views.order_add, name='order_add'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    
    path('customers/', views.customer_list, name='customers'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    path('suppliers/', views.supplier_list, name='suppliers'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    path('stock/', views.stock_list, name='stock'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    
    path('settings/', views.settings, name='settings'),
]
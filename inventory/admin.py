from django.contrib import admin
from .models import (
    InventoryItem, Category, Supplier, Room,
    HousekeepingTask, InventoryUsage
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'email')
    list_filter = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'status', 'last_cleaned', 'next_cleaning')
    list_filter = ('room_type', 'status')
    search_fields = ('room_number', 'notes')
    ordering = ('room_number',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'quantity', 'minimum_quantity', 'unit_price',
        'category', 'item_type', 'supplier', 'expiry_date',
        'is_low_stock'
    )
    list_filter = ('category', 'item_type', 'supplier')
    search_fields = ('name', 'description', 'location')
    ordering = ('name',)
    date_hierarchy = 'expiry_date'


@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    list_display = (
        'room', 'assigned_to', 'status', 'scheduled_time',
        'completed_time'
    )
    list_filter = ('status', 'assigned_to')
    search_fields = ('room__room_number', 'notes')
    ordering = ('-scheduled_time',)
    date_hierarchy = 'scheduled_time'


@admin.register(InventoryUsage)
class InventoryUsageAdmin(admin.ModelAdmin):
    list_display = (
        'item', 'quantity_used', 'room', 'used_by',
        'date_used'
    )
    list_filter = ('used_by', 'room')
    search_fields = ('item__name', 'notes')
    ordering = ('-date_used',)
    date_hierarchy = 'date_used'

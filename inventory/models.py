from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Category(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name


class Supplier(models.Model):
	name = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	email = models.EmailField()
	address = models.TextField()
	notes = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Room(models.Model):
	ROOM_STATUS = [
		('available', 'Available'),
		('occupied', 'Occupied'),
		('maintenance', 'Maintenance'),
		('cleaning', 'Cleaning'),
	]
	
	ROOM_TYPES = [
		('standard', 'Standard'),
		('deluxe', 'Deluxe'),
		('suite', 'Suite'),
		('presidential', 'Presidential'),
	]

	room_number = models.CharField(max_length=10, unique=True)
	room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
	status = models.CharField(max_length=20, choices=ROOM_STATUS, default='available')
	last_cleaned = models.DateTimeField(null=True, blank=True)
	next_cleaning = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		return f"Room {self.room_number} - {self.get_room_type_display()}"


class InventoryItem(models.Model):
	ITEM_TYPES = [
		('room', 'Room Supplies'),
		('housekeeping', 'Housekeeping'),
		('food', 'Food & Beverage'),
		('maintenance', 'Maintenance'),
		('uniform', 'Staff Uniforms'),
		('amenity', 'Guest Amenities'),
	]

	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	minimum_quantity = models.IntegerField(default=5)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
	item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='room')
	supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
	expiry_date = models.DateField(null=True, blank=True)
	location = models.CharField(max_length=200, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	@property
	def is_low_stock(self):
		return self.quantity <= self.minimum_quantity


class HousekeepingTask(models.Model):
	TASK_STATUS = [
		('pending', 'Pending'),
		('in_progress', 'In Progress'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	]

	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	status = models.CharField(max_length=20, choices=TASK_STATUS, default='pending')
	scheduled_time = models.DateTimeField()
	completed_time = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Housekeeping for {self.room} - {self.get_status_display()}"


class InventoryUsage(models.Model):
	item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
	quantity_used = models.IntegerField(validators=[MinValueValidator(1)])
	room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
	used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date_used = models.DateTimeField(auto_now_add=True)
	notes = models.TextField(blank=True)

	def __str__(self):
		return f"{self.quantity_used} {self.item.name} used in {self.room if self.room else 'General'}"
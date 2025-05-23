from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, Supplier, Room, HousekeepingTask, InventoryUsage, Product, Order, Customer, Stock

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'description']

class SupplierForm(forms.ModelForm):
	class Meta:
		model = Supplier
		fields = ['name', 'contact_person', 'phone', 'email', 'address', 'notes']

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['room_number', 'room_type', 'status', 'notes']
		widgets = {
			'notes': forms.Textarea(attrs={'rows': 3}),
		}

class InventoryItemForm(forms.ModelForm):
	class Meta:
		model = InventoryItem
		fields = [
			'name', 'description', 'quantity', 'minimum_quantity', 'unit_price',
			'category', 'item_type', 'supplier', 'expiry_date', 'location'
		]
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3}),
			'expiry_date': forms.DateInput(attrs={'type': 'date'}),
		}

class HousekeepingTaskForm(forms.ModelForm):
	class Meta:
		model = HousekeepingTask
		fields = ['room', 'assigned_to', 'status', 'scheduled_time', 'notes']
		widgets = {
			'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
			'notes': forms.Textarea(attrs={'rows': 3}),
		}

class InventoryUsageForm(forms.ModelForm):
	class Meta:
		model = InventoryUsage
		fields = ['item', 'quantity_used', 'room', 'notes']
		widgets = {
			'notes': forms.Textarea(attrs={'rows': 3}),
		}

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['productName', 'description', 'price', 'stockQuantity', 'categoryID']
		labels = {
			'productName': 'Product Name',
			'description': 'Description',
			'price': 'Price',
			'stockQuantity': 'Stock Quantity',
			'categoryID': 'Category'
		}

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['customerID', 'orderDate', 'totalAmount']
		labels = {
			'customerID': 'Customer',
			'orderDate': 'Order Date',
			'totalAmount': 'Total Amount'
		}
		widgets = {
			'orderDate': forms.DateInput(attrs={'type': 'date'})
		}

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['customerName', 'contactInfo', 'address']
		labels = {
			'customerName': 'Customer Name',
			'contactInfo': 'Contact Information',
			'address': 'Address'
		}

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['productID', 'quantity', 'costPrice', 'stockDate']
		labels = {
			'productID': 'Product',
			'quantity': 'Quantity',
			'costPrice': 'Cost Price',
			'stockDate': 'Stock Date'
		}
		widgets = {
			'stockDate': forms.DateInput(attrs={'type': 'date'})
		}
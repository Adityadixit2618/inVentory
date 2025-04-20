from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.utils import timezone
from .forms import (
	UserRegisterForm, InventoryItemForm, CategoryForm, SupplierForm,
	RoomForm, HousekeepingTaskForm, InventoryUsageForm
)
from .models import (
	InventoryItem, Category, Supplier, Room, HousekeepingTask,
	InventoryUsage
)
from inventory_management.settings import LOW_QUANTITY

class Index(TemplateView):
	template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		# Inventory Overview
		items = InventoryItem.objects.filter(user=request.user).order_by('id')
		low_stock_items = items.filter(quantity__lte=F('minimum_quantity'))
		expiring_items = items.filter(expiry_date__lte=timezone.now() + timezone.timedelta(days=30))
		
		# Room Status
		rooms = Room.objects.all()
		available_rooms = rooms.filter(status='available').count()
		occupied_rooms = rooms.filter(status='occupied').count()
		
		# Housekeeping Tasks
		pending_tasks = HousekeepingTask.objects.filter(
			status='pending',
			scheduled_time__lte=timezone.now() + timezone.timedelta(hours=24)
		)
		
		# Recent Inventory Usage
		recent_usage = InventoryUsage.objects.order_by('-date_used')[:5]
		
		context = {
			'items': items,
			'low_stock_items': low_stock_items,
			'expiring_items': expiring_items,
			'rooms': rooms,
			'available_rooms': available_rooms,
			'occupied_rooms': occupied_rooms,
			'pending_tasks': pending_tasks,
			'recent_usage': recent_usage,
		}
		
		return render(request, 'inventory/dashboard.html', context)

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)
			login(request, user)
			return redirect('index')
		return render(request, 'inventory/signup.html', {'form': form})

class InventoryItemListView(LoginRequiredMixin, ListView):
	model = InventoryItem
	template_name = 'inventory/inventory_list.html'
	context_object_name = 'items'

	def get_queryset(self):
		return InventoryItem.objects.filter(user=self.request.user)

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('inventory_list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		messages.success(self.request, 'Item added successfully!')
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('inventory_list')

	def form_valid(self, form):
		messages.success(self.request, 'Item updated successfully!')
		return super().form_valid(form)

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('inventory_list')
	context_object_name = 'item'

class RoomListView(LoginRequiredMixin, ListView):
	model = Room
	template_name = 'inventory/room_list.html'
	context_object_name = 'rooms'

class AddRoom(LoginRequiredMixin, CreateView):
	model = Room
	form_class = RoomForm
	template_name = 'inventory/room_form.html'
	success_url = reverse_lazy('room_list')

	def form_valid(self, form):
		messages.success(self.request, 'Room added successfully!')
		return super().form_valid(form)

class EditRoom(LoginRequiredMixin, UpdateView):
	model = Room
	form_class = RoomForm
	template_name = 'inventory/room_form.html'
	success_url = reverse_lazy('room_list')

	def form_valid(self, form):
		messages.success(self.request, 'Room updated successfully!')
		return super().form_valid(form)

class HousekeepingTaskListView(LoginRequiredMixin, ListView):
	model = HousekeepingTask
	template_name = 'inventory/task_list.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return HousekeepingTask.objects.filter(
			scheduled_time__gte=timezone.now() - timezone.timedelta(days=7)
		).order_by('scheduled_time')

class AddTask(LoginRequiredMixin, CreateView):
	model = HousekeepingTask
	form_class = HousekeepingTaskForm
	template_name = 'inventory/task_form.html'
	success_url = reverse_lazy('task_list')

	def form_valid(self, form):
		messages.success(self.request, 'Task added successfully!')
		return super().form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
	model = HousekeepingTask
	form_class = HousekeepingTaskForm
	template_name = 'inventory/task_form.html'
	success_url = reverse_lazy('task_list')

	def form_valid(self, form):
		if form.instance.status == 'completed':
			form.instance.completed_time = timezone.now()
		messages.success(self.request, 'Task updated successfully!')
		return super().form_valid(form)

class RecordUsage(LoginRequiredMixin, CreateView):
	model = InventoryUsage
	form_class = InventoryUsageForm
	template_name = 'inventory/usage_form.html'
	success_url = reverse_lazy('dashboard')

	def form_valid(self, form):
		form.instance.used_by = self.request.user
		item = form.instance.item
		item.quantity -= form.instance.quantity_used
		item.save()
		messages.success(self.request, 'Usage recorded successfully!')
		return super().form_valid(form)

class ReportsView(LoginRequiredMixin, View):
	def get(self, request):
		# Inventory Value
		total_value = InventoryItem.objects.filter(
			user=request.user
		).aggregate(
			total=Sum(F('quantity') * F('unit_price'))
		)['total'] or 0

		# Low Stock Items
		low_stock_items = InventoryItem.objects.filter(
			user=request.user,
			quantity__lte=F('minimum_quantity')
		)

		# Expiring Items
		expiring_items = InventoryItem.objects.filter(
			user=request.user,
			expiry_date__lte=timezone.now() + timezone.timedelta(days=30)
		)

		# Room Occupancy
		room_stats = {
			'total': Room.objects.count(),
			'available': Room.objects.filter(status='available').count(),
			'occupied': Room.objects.filter(status='occupied').count(),
			'maintenance': Room.objects.filter(status='maintenance').count(),
		}

		context = {
			'total_value': total_value,
			'low_stock_items': low_stock_items,
			'expiring_items': expiring_items,
			'room_stats': room_stats,
		}
		return render(request, 'inventory/reports.html', context)

def logout_view(request):
	"""Custom logout view that handles both GET and POST requests."""
	if request.method == 'POST':
		logout(request)
		messages.success(request, 'You have been successfully logged out.')
		return redirect('login')
	elif request.method == 'GET':
		return render(request, 'inventory/logout.html')

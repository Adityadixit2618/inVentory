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
	RoomForm, HousekeepingTaskForm, InventoryUsageForm, ProductForm, OrderForm, CustomerForm, StockForm
)
from .models import (
	InventoryItem, Category, Supplier, Room, HousekeepingTask,
	InventoryUsage, Product, Order, OrderDetails, Customer, Stock
)
from inventory_management.settings import LOW_QUANTITY
from django.contrib.auth.decorators import login_required

class Index(TemplateView):
	template_name = 'inventory/index.html'

@login_required
def dashboard(request):
	total_products = Product.objects.count()
	total_orders = Order.objects.count()
	total_customers = Customer.objects.count()
	low_stock_products = Product.objects.filter(stockquantity__lt=10)
	
	context = {
		'total_products': total_products,
		'total_orders': total_orders,
		'total_customers': total_customers,
		'low_stock_products': low_stock_products,
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

# Product Views
@login_required
def product_list(request):
	products = Product.objects.all()
	return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def product_add(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Product added successfully.')
			return redirect('products')
	else:
		form = ProductForm()
	return render(request, 'inventory/product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			messages.success(request, 'Product updated successfully.')
			return redirect('products')
	else:
		form = ProductForm(instance=product)
	return render(request, 'inventory/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
	product = get_object_or_404(Product, pk=pk)
	product.delete()
	messages.success(request, 'Product deleted successfully.')
	return redirect('products')

# Category Views
@login_required
def category_list(request):
	categories = Category.objects.all()
	return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
def category_add(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Category added successfully.')
			return redirect('categories')
	else:
		form = CategoryForm()
	return render(request, 'inventory/category_form.html', {'form': form})

@login_required
def category_edit(request, pk):
	category = get_object_or_404(Category, pk=pk)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			messages.success(request, 'Category updated successfully.')
			return redirect('categories')
	else:
		form = CategoryForm(instance=category)
	return render(request, 'inventory/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
	category = get_object_or_404(Category, pk=pk)
	category.delete()
	messages.success(request, 'Category deleted successfully.')
	return redirect('categories')

# Order Views
@login_required
def order_list(request):
	orders = Order.objects.all().order_by('-orderDate')
	return render(request, 'inventory/order_list.html', {'orders': orders})

@login_required
def order_add(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Order added successfully.')
			return redirect('orders')
	else:
		form = OrderForm()
	return render(request, 'inventory/order_form.html', {'form': form})

@login_required
def order_detail(request, pk):
	order = get_object_or_404(Order, pk=pk)
	return render(request, 'inventory/order_detail.html', {'order': order})

@login_required
def order_edit(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			messages.success(request, 'Order updated successfully.')
			return redirect('orders')
	else:
		form = OrderForm(instance=order)
	return render(request, 'inventory/order_form.html', {'form': form})

# Customer Views
@login_required
def customer_list(request):
	customers = Customer.objects.all()
	return render(request, 'inventory/customer_list.html', {'customers': customers})

@login_required
def customer_add(request):
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Customer added successfully.')
			return redirect('customers')
	else:
		form = CustomerForm()
	return render(request, 'inventory/customer_form.html', {'form': form})

@login_required
def customer_edit(request, pk):
	customer = get_object_or_404(Customer, pk=pk)
	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			messages.success(request, 'Customer updated successfully.')
			return redirect('customers')
	else:
		form = CustomerForm(instance=customer)
	return render(request, 'inventory/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
	customer = get_object_or_404(Customer, pk=pk)
	customer.delete()
	messages.success(request, 'Customer deleted successfully.')
	return redirect('customers')

# Supplier Views
@login_required
def supplier_list(request):
	suppliers = Supplier.objects.all()
	return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_add(request):
	if request.method == 'POST':
		form = SupplierForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Supplier added successfully.')
			return redirect('suppliers')
	else:
		form = SupplierForm()
	return render(request, 'inventory/supplier_form.html', {'form': form})

@login_required
def supplier_edit(request, pk):
	supplier = get_object_or_404(Supplier, pk=pk)
	if request.method == 'POST':
		form = SupplierForm(request.POST, instance=supplier)
		if form.is_valid():
			form.save()
			messages.success(request, 'Supplier updated successfully.')
			return redirect('suppliers')
	else:
		form = SupplierForm(instance=supplier)
	return render(request, 'inventory/supplier_form.html', {'form': form})

@login_required
def supplier_delete(request, pk):
	supplier = get_object_or_404(Supplier, pk=pk)
	supplier.delete()
	messages.success(request, 'Supplier deleted successfully.')
	return redirect('suppliers')

# Stock Views
@login_required
def stock_list(request):
	stock_items = Stock.objects.all()
	return render(request, 'inventory/stock_list.html', {'stock_items': stock_items})

@login_required
def stock_add(request):
	if request.method == 'POST':
		form = StockForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Stock added successfully.')
			return redirect('stock')
	else:
		form = StockForm()
	return render(request, 'inventory/stock_form.html', {'form': form})

@login_required
def stock_edit(request, pk):
	stock = get_object_or_404(Stock, pk=pk)
	if request.method == 'POST':
		form = StockForm(request.POST, instance=stock)
		if form.is_valid():
			form.save()
			messages.success(request, 'Stock updated successfully.')
			return redirect('stock')
	else:
		form = StockForm(instance=stock)
	return render(request, 'inventory/stock_form.html', {'form': form})

@login_required
def reports(request):
	return render(request, 'inventory/reports.html')

@login_required
def settings(request):
	return render(request, 'inventory/settings.html')

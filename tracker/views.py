from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Vehicle
from .forms import VehicleForm, SignupForm
from django.db.models import Sum
from django.db.models import Q, Sum

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    vehicles = Vehicle.objects.filter(user=request.user)

    overdue = [v for v in vehicles if v.status == 'Overdue']
    due_soon = [v for v in vehicles if v.status == 'Due soon']

    total_spent = ServiceRecord.objects.filter(
        vehicle__user=request.user
    ).aggregate(total=Sum('cost'))['total'] or 0

    return render(request, 'tracker/home.html', {
        'total_vehicles': vehicles.count(),
        'overdue': overdue,
        'due_soon': due_soon,
        'total_spent': total_spent,
    })


@login_required
def vehicle_list(request):
    q = request.GET.get('q', '').strip()
    vehicles = Vehicle.objects.filter(user=request.user)
    if q:
        vehicles = vehicles.filter(Q(name__icontains=q) | Q(number__icontains=q))
    return render(request, 'tracker/vehicle_list.html', {'vehicles': vehicles, 'q': q})

@login_required
def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'tracker/vehicle_form.html', {'form': form})


from django.shortcuts import get_object_or_404
from .models import ServiceRecord
from .forms import ServiceRecordForm

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    records = vehicle.records.all()
    return render(request, 'tracker/vehicle_detail.html', {
        'vehicle': vehicle,
        'records': records,
    })

@login_required
def service_add(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.vehicle = vehicle
            record.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = ServiceRecordForm()
    return render(request, 'tracker/service_form.html', {'form': form, 'vehicle': vehicle})

@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'tracker/vehicle_form.html', {'form': form, 'title': 'Edit Vehicle'})


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'tracker/confirm_delete.html', {
        'message': f'"{vehicle.name}" and all its service records will be deleted.',
        'cancel_url': 'vehicle_detail',
        'cancel_pk': vehicle.pk,
    })


@login_required
def service_edit(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, vehicle__user=request.user)
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('vehicle_detail', pk=record.vehicle.pk)
    else:
        form = ServiceRecordForm(instance=record)
    return render(request, 'tracker/service_form.html', {
        'form': form,
        'vehicle': record.vehicle,
        'title': 'Edit Service',
    })


@login_required
def service_delete(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk, vehicle__user=request.user)
    vehicle = record.vehicle
    if request.method == 'POST':
        record.delete()
        return redirect('vehicle_detail', pk=vehicle.pk)
    return render(request, 'tracker/confirm_delete.html', {
        'message': f'Service record of {record.service_date} will be deleted.',
        'cancel_url': 'vehicle_detail',
        'cancel_pk': vehicle.pk,
    })


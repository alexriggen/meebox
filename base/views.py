from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Entry, Month, fileModel
from .forms import MonthForm, fileForm, entryForm, MonthComparisonForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect


# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html')

@login_required
def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    if query:
        months = Month.objects.filter(name__icontains=query)
    else:
        months = Month.objects.all()
    
    context = {'months': months}
    return render(request, 'home.html', context)

@login_required
def other(request, month_id):
    month = Month.objects.get(pk=month_id)

    query = request.GET.get('q') if request.GET.get('q') != None else ''
    if query:
        entries = Entry.objects.filter(Q(concepto__icontains=query) | Q(description__icontains=query))
    else:
        entries = Entry.objects.all()
    
    entries = entries.filter(month=month)
    cargo_total = 0
    abono_total = 0

    for entry in entries:
        if entry.cargo:
            cargo_total += (float(entry.cargo.replace(",", "")))
        if entry.abono:
            abono_total += (float(entry.abono.replace(",", "")))

    request.session['month_id'] = month.id
    return render(request, 'other.html', {'month': month, 'entries': entries, 'month_id': month_id,'abono_total':round(abono_total,2),'cargo_total':round(cargo_total,2)})

@login_required
def editMonth(request, pk):
    month = Month.objects.get(id=pk)
    form = MonthForm(instance = month)
    if request.method == 'POST':
        form = MonthForm(request.POST, instance=month)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'entry_mod_form.html',context)

@login_required
def editEntry(request, pk):
    month_id = request.session.get('month_id')
    entry = Entry.objects.get(id=pk)
    form = entryForm(instance = entry)
    if request.method == 'POST':
        form = entryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('other', month_id=month_id)
    context = {'form': form}
    return render(request, 'movimiento_edit.html',context)

@login_required
def addMonth(request):
    form = MonthForm()
    if request.method == 'POST':
        form = MonthForm(request.POST)
        if form.is_valid():
            month = form.save(commit=False)  
            month.creator = request.user  
            month.save()  
            request.session['month_id'] = month.id
            return redirect('addentries')  
            

    context = {'form': form}
    return render(request,'entry_mod_form.html',context)

@login_required
def addEntries(request):

#GET MONTH
    month_id = request.session.get('month_id')
    if not month_id:
        return redirect('home')  

    try:
        month = Month.objects.get(pk=month_id)
    except Month.DoesNotExist:
        return redirect('home')

#FILE HANDLING
    file_content = None
    
    if request.method == 'POST':
        form = fileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Save the model instance and file
            file_path = instance.file.path
            with open(file_path, 'r') as file:
                lines = file.readlines()
                csv_file = [['Dia','Concepto/Referencia','Cargo','Abono','Saldo']]
                for line in lines[1:]:
                    new_entry = []
                    column = line.split('\t')
                    for element in column:
                        stripped_element = element.replace('\n','')
                        new_entry.append(stripped_element)
                    csv_file.append(new_entry)

            for row in csv_file[1:]:
                date, concepto, abono, cargo ,saldo = row
                Entry.objects.create(
                    creator=request.user,
                    month=month,
                    date=date,
                    concepto = concepto,
                    cargo=cargo,
                    abono=abono,
                    saldo = saldo,
                    description="",
                )
            return redirect('home')            

    else:
        form = fileForm()

    context = {'month':month,'form': form, 'file_content': file_content}
    return render(request, 'add_entries.html', context)

@login_required
def comparar(request):
    entries_month1 = []
    entries_month2 = []
    month1 = month2 = None

    if request.method == 'POST':
        form = MonthComparisonForm(request.POST)
        if form.is_valid():
            month1 = form.cleaned_data.get('month1')
            month2 = form.cleaned_data.get('month2')
            if month1:
                entries_month1 = Entry.objects.filter(month=month1)
            if month2:
                entries_month2 = Entry.objects.filter(month=month2)
    else:
        form = MonthComparisonForm()

    context = {
        'form': form,
        'entries_month1': entries_month1,
        'entries_month2': entries_month2,
        'month1': month1,
        'month2': month2,
    }
    return render(request,'compare.html',context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import csv
from django.http import HttpResponse
import string
import time


def login_user(request):
    logout(request)
    try:
        if request.user.is_authenticated:
            return redirect('/dashboard/')

        if request.method == "POST":
            username = request.POST['username']
            userpassword = request.POST['password']
            myuser = User.objects.filter(username = username)
            if not myuser.exists():
                messages.warning(request,"Invalid Credentials")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            myuser = authenticate (username = username, password=userpassword)
            if myuser is not None:
                if myuser.is_staff or myuser.is_superuser:
                    login(request, myuser)
                    return redirect(request.POST.get('next', '/dashboard/'))
                else:
                    messages.warning(request, 'User not Access')
                    return redirect('/')
            else:
                messages.warning(request, 'Invalid Password')
                return redirect('/')

        return render(request,'login.html')
    except Exception as e:
        print(e)

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def index(request):
    products = Product.objects.filter(status = 1).all()
    tempproducts = Tempitem.objects.all()
    total_price = Tempitem.objects.aggregate(total_price=models.Sum('temptotal'))
    context={
                'products': products,
                'bill_items': tempproducts,
                'total_price': total_price,
            }
    return render(request, 'index.html', context)

@login_required
def add(request):
    if request.method == 'POST':
        selected_items = request.POST.get('pid')
        if selected_items is None:
            messages.warning(request, f'Select the item.')
            return redirect('/dashboard/')
        price = Product.objects.filter(name = selected_items).values('price')
        quntity = Product.objects.filter(name = selected_items).values('totalquantity')
        quntity = quntity[0]['totalquantity']
        price = price[0]['price']
        quantities = request.POST.get('quantity')
        cost = float(price) * int(quantities)
        products = Product.objects.filter(status = 1).all()

        if int(quantities) <= quntity :
            try:
                item = Tempitem.objects.filter(tempname=selected_items).get()
                item.tempprice = price
                item.tempquntity = quantities
                item.temptotal = cost
                item.save()
            except Tempitem.DoesNotExist:
                item = Tempitem.objects.create(tempname=selected_items, tempprice=price, tempquntity=quantities, temptotal=cost)

            tempproducts = Tempitem.objects.all()
            total_price = Tempitem.objects.aggregate(total_price=models.Sum('temptotal'))
            context={
                'products': products,
                'bill_items': tempproducts,
                'total_price': total_price,
            }
            return redirect('/dashboard/', context)
        else:
            messages.warning(request, f'Maxmimum quntity of {selected_items} item is {quntity}.')
            return redirect('/dashboard/')

@login_required
def delete(request):
    Tempitem.objects.all().delete()
    CustomerBill.objects.all().delete()
    return redirect('/dashboard/')

@login_required
def delete_item(request, id):
    if request.method == "POST":
        item = Tempitem.objects.get(tempname=id)
        item.delete()
        return redirect('/dashboard/')

@login_required
def create_bill(request):
    items = Tempitem.objects.all()
    if not items:
        messages.warning(request, 'Enter items in  bill.')
        return redirect('/dashboard/')
    totalitems = Tempitem.objects.aggregate(total=Sum('tempquntity'))
    totalprice = Tempitem.objects.aggregate(total=Sum('temptotal'))
    if request.method == "POST":
        custname = request.POST.get('custname')
        custnumb = request.POST.get('custmobile')
        payment = request.POST.get('payment')
        if custname == '' or custnumb == '':
            messages.warning(request, 'Enter the Customer Detials.')
            return redirect('/dashboard/')

    pref = datetime.today().strftime('%Y%m%d')
    date = datetime.today()
    last_bill = CustomerBill.objects.order_by('-itemcode').first()
    last_transactional_code = last_bill.itemcode if last_bill else ''
    last_date = int(last_transactional_code[:8]) if last_transactional_code else 0
    last_sequence = int(last_transactional_code[-4:]) + 1 if last_transactional_code else 1
    if last_date == int(pref):
        transactionalcode = pref + str(last_sequence).zfill(4)
    else:
        transactionalcode = pref + "0001"

    for item in items:
        bill = invoiceitem()
        bill.itemname = item.tempname
        bill.itemprice = item.tempprice
        bill.itemquntity = item.tempquntity
        bill.itemtotal = item.temptotal
        bill.itemcode = transactionalcode
        bill.save()

    for item in items:
        bill = stockhistory()
        bill.itemname = item.tempname
        bill.itemquntity = item.tempquntity
        bill.status = 2
        bill.save()

    for item in items:
        update_product_quantity(item.tempname , item.tempquntity)

    CustomerBill.objects.create(custname=custname, custnumb=custnumb, totalitem =totalitems['total'], totalprice=totalprice['total'], itemcode = transactionalcode, payment=payment)
    Tempitem.objects.all().delete()
    data = invoiceitem.objects.filter(itemcode=transactionalcode)
    context = {'custname': custname, 'custnumb': custnumb, 'totalprice': totalprice, 'totalitem': totalitems, 'itemcode': transactionalcode, 'data': data, 'date': date, 'payment': payment}
    return render(request, 'pdf.html', context)

@login_required
def pdf(request):
    slr = CustomerBill.objects.last()
    return render(request,'pdf.html',{'seller':slr})

@login_required
def viewpdf(request, code):
    data = CustomerBill.objects.filter(itemcode=code)
    item = invoiceitem.objects.filter(itemcode=code)
    context = {'data':data, 'item':item}
    return render(request,'viewpdf.html',context)

def update_product_quantity(itemname, itemquntity):
    product = get_object_or_404(Product, name=itemname)
    product.totalquantity -= itemquntity
    product.save()

@login_required
def product(request):
    product = AddProduct()
    context = {'form':product}
    return render(request, 'product.html',context)

@login_required
def save_product(request):
    if request.method == "POST":
        form = AddProduct(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            if not Product.objects.filter(name=product_name).exists():
                form.save()
                messages.success(request, 'Product saved successfully.')
            else:
                messages.warning(request, 'Product with the same name already exists.')
        return redirect('/product/')

@login_required
def view_product(request):
    product = Product.objects.all()
    myfilter = ProductFilter(request.GET, queryset=product)
    product = myfilter.qs
    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {"product": products, 'form': EditProduct(), 'filter': myfilter}
    return render(request, 'view_product.html', context)

@login_required
def edit_product(request, name):
    product = Product.objects.get(name=name)
    if request.method == "POST":
        product = Product.objects.get(name=name)
        form = EditProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Update Successfully.')
            return redirect('/viewproduct/')
    else:
        product = Product.objects.get(name=name)
        form = EditProduct(instance=product)
    return render(request, 'editproduct.html',{'form': form})

@login_required
def delete_product(request, name):
    if request.method == "POST":
        product = Product.objects.get(name=name)
        product.delete()
        messages.success(request, 'Delete Product Successfully.')
    return redirect('/viewproduct/')

@login_required
def show_product(request, name):
    product = Product.objects.get(name=name)
    stock = stockhistory.objects.filter(itemname=name)
    paginator = Paginator(stock, 10)
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    if stock:
        context = {'product': product, 'stocks': stocks}
    else:
        context = {'product': product}
    return render(request, 'showproduct.html', context)

@login_required
def add_stock(request, name):
    product = Product.objects.get(name=name)
    products = Product.objects.filter(name=name).values('totalquantity')
    total = products[0]['totalquantity']
    if request.method == "POST":
        quantity = request.POST.get('quntity')
        check = request.POST.get('check')
        if check == "checked":
            total -= int(quantity)
            product.totalquantity = total
            product.save()
            new_stock = stockhistory(itemname = name, itemquntity = quantity, status = 2)
            new_stock.save()
            messages.success(request, 'Remove Stock Successfully.')
        else:
            total += int(quantity)
            product.totalquantity = total
            product.save()
            new_stock = stockhistory(itemname = name, itemquntity = quantity, status = 1)
            new_stock.save()
            messages.success(request, 'Add Stock Successfully.')
    return redirect('/viewproduct/')

@login_required
def customer(request):
    customer = CustomerBill.objects.all()
    myfilter = CustomerFilter(request.GET, queryset=customer)
    customer = myfilter.qs
    paginator = Paginator(customer, 10)
    page = request.GET.get('page')
    customer = paginator.get_page(page)
    context = {'customer':customer, 'form': EditCustomer(), 'filter':myfilter}
    return render(request, 'customer.html', context)

@login_required
def edit_customer(request, code):
    customer = CustomerBill.objects.get(itemcode = code)
    if request.method == "POST":
        customer = CustomerBill.objects.get(itemcode = code)
        form = EditCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Update Successfully.')
            return redirect('/customer/')
    else:
        customer = CustomerBill.objects.get(itemcode = code)
        form = EditCustomer(instance=customer)
    return render(request, 'editcustomer.html',{'form': form})

def upload_csv(request):
    if request.method == "POST":
            csv_file = request.FILES.get('csv_file')
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
                next(csv_data)
                raw_list = []

                for row in csv_data:
                    name = row[0]
                    name = string.capwords(name, sep=None)
                    price = float(row[1])
                    quntity = int(row[2])
                    description = row[3]

                if name == "":
                    raw_list = []
                    messages.warning(request, 'Product Name is not available in CSV File')
                    return redirect('/product/')

                if quntity<1000:
                    raw_list.append(name)
                    raw_list.append(price)
                    raw_list.append(quntity)
                    raw_list.append(description)
                else:
                    raw_list = []
                    messages.warning(request, 'CSV File Quantity is more than 1000')
                    return redirect('/product/')

                print(raw_list)
                if raw_list is not None:
                    update_csv(raw_list)
                else:
                    messages.success(request, 'Add CSV File With Product Data Rows')
                    return redirect('/product/')
                messages.success(request, 'All Product saved successfully.')
                return redirect('/product/')

            except Exception as e:
                messages.warning(request, 'Enter the CSV File.')
                return redirect('/product/')


def download_csv(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=sample.csv'
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Price', 'Quantity', 'Description'])

    return response


def update_csv(raw_list):
    for i in range(0, len(raw_list), 4):
        name = raw_list[i]
        price = raw_list[i + 1]
        quntity = raw_list[i + 2]
        description = raw_list[i + 3]

        if not Product.objects.filter(name=name).exists():
            product = Product(name=name, price=price, description=description, totalquantity=quntity)
            product.save()
            new_stock = stockhistory(itemname = name, itemquntity = quntity, status = 1)
            new_stock.save()
        else:
            product = Product.objects.get(name=name)
            products = Product.objects.filter(name=name).values('totalquantity')
            total = products[0]['totalquantity']
            total += int(quntity)
            product.totalquantity = total
            product.save()
            new_stock = stockhistory(itemname = name, itemquntity = quntity, status = 1)
            new_stock.save()





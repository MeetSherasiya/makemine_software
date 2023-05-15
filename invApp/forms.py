from django import forms
from .models import *

class AddProduct(forms.ModelForm):
    name=models.CharField(max_length=350,blank=True, null=True)
    description = models.TextField()
    totalquantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    class Meta:
        model = Product
        fields = ('name','description','totalquantity','price','status')
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'totalquantity': 'Quantity',
            'price': 'Price',
            'status': 'Status'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'null': 'True', 'rows': 4}),
            'totalquantity': forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '1000'}),
            'price': forms.NumberInput(attrs={'class':'form-control' , 'min':'0'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }

class EditProduct(forms.ModelForm):
    name=models.CharField(max_length=350,blank=True, null=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    class Meta:
        model = Product
        fields = ('name','description','price','status')
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'status': 'Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'null': 'True'}),
            'price': forms.NumberInput(attrs={'class':'form-control' , 'min':'0'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }
    
class EditCustomer(forms.ModelForm):
    custname = models.CharField(max_length=350)
    custnumb = models.IntegerField(default = 0 ,null=True, blank=True)
    payment = models.CharField(max_length=2, choices=(('1','Cash'),('2','Online'),('3','Pending')), default=1)

    class Meta:
        model = CustomerBill
        fields = ('custname', 'custnumb','payment')
        labels = {
            'custname': 'Customer Name',
            'custnumb': 'Customer No.',
            'payment': 'Payment',
        }
        widgets = {
            'custname': forms.TextInput(attrs={'class':'form-control'}),
            'custnumb': forms.NumberInput(attrs={'class':'form-control'}),
            'payment': forms.Select(attrs={'class':'form-control'}),
        }
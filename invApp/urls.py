from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name="login_user"),
    path('logout/', logout_user, name="logout"),
    path('dashboard/', index, name="Index"),
    path('product/', product, name="product"),
    path('csv/', upload_csv, name="upload_csv"),
    path('downloadcsv/', download_csv, name="download_csv"),
    path('viewproduct/', view_product, name="viewproduct"),
    path('addstock/<str:name>/', add_stock, name="addstock"),
    path('editproduct/<str:name>/', edit_product, name="editproduct"),
    path('showproduct/<str:name>/', show_product, name="showproduct"),
    path('deleteproduct/<str:name>/', delete_product, name="deleteproduct"),
    path('saveproduct/', save_product, name="saveproduct"),
    path('add/', add, name="Additem"),
    path('delete/', delete, name="Deleteitem"),
    path('delete/<str:id>/', delete_item, name="Deletetempitem"),
    path('createbill/', create_bill, name="Createbill"),
    path('pdf/', pdf, name="pdf"),
    path('viewpdf/<str:code>/', viewpdf, name="viewpdf"),
    path('customer/', customer, name="customer"),
    path('editcustomer/<str:code>/', edit_customer, name="editcustomer"),
]
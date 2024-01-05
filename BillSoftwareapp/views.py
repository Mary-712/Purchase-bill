# Name: Mary C Wilson

from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from . models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from BillSoftwareapp .models import ItemModel,Parties,staff_details,company,FirstBill
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
# Create your views here.

def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')


def service(request):
  return render(request, 'service.html')


def homepage(request):
  return render(request, 'companyhome.html')


def staffhome(request):
  return render(request, 'staffhome.html')

def register(request):
  return render(request, 'register.html')

def registercompany(request):
  return render(request, 'registercompany.html')

def registerstaff(request):
  return render(request, 'registerstaff.html')

def login(request):
  return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def base(request):
  return render(request, 'base.html')

def registeruser(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['username']
        email_id = request.POST['email']
        mobile = request.POST['phoneno']
        passw = request.POST['pass']
        c_passw = request.POST['re_pass']
        profile_pic=request.FILES.get('image')

        if passw != c_passw:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Sorry, Username already exists')
            return redirect('register')

        if User.objects.filter(email=email_id).exists():
            messages.error(request, 'Sorry, Email already exists')
            return redirect('register')

        # If everything is okay, save the data
        user_data = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=user_name,
            email=email_id,
            password=passw
        )
        user_data.save()

        data = User.objects.get(id=user_data.id)
        cust_data = company(contact=mobile,profile_pic=profile_pic, user=data)
        cust_data.save()

        demo_staff=staff_details(company=cust_data,
                                   email=email_id,
                                   position='company',
                                   user_name=user_name,
                                   password=passw,
                                   contact=mobile)
        demo_staff.save()

        # messages.success(request, 'Registration successful')
        return redirect('registercompany')

    return render(request, 'register.html')
  
def add_company(request):
  
  if request.method == 'POST':
    email=request.POST['email']
    user=User.objects.get(email=email)
    
    c =company.objects.get(user = user)
    c.company_name=request.POST['companyname']

    c.address=request.POST['address']
    c.city=request.POST['city']
    c.state=request.POST['state']
    c.country=request.POST['country']
    c.pincode=request.POST['pincode']
    c.pan_number=request.POST['pannumber']
    c.gst_type=request.POST['gsttype']
    c.gst_no=request.POST['gstno']

    code=get_random_string(length=6)
    if company.objects.filter(Company_code = code).exists():
       code2=get_random_string(length=6)
       c.Company_code=code2
    else:
      c.Company_code=code
   
    c.save()

    staff = staff_details.objects.get(email=email,position='company',company=c)
    staff.first_name = request.POST['companyname']
    staff.last_name = ''
    staff.save()

    return redirect('login')  
  return render(request,'registercompany.html') 

def staff_registraction(request):
  if request.method == 'POST':
    fn=request.POST['fname']
    ln=request.POST['lname']
    email=request.POST['email']
    un=request.POST['username']
    ph=request.POST['phoneno']
    pas=request.POST['pass']
    code=request.POST['companycode']

    if company.objects.filter(Company_code=code).exists():
      com=company.objects.get(Company_code=code)
    else:
        messages.info(request, 'Sorry, Company code is Invalide')
        return redirect('registerstaff')
    img=request.FILES.get('image')

    if staff_details.objects.filter(user_name=un).exists():
      messages.info(request, 'Sorry, Username already exists')
      return redirect('registerstaff')
    elif staff_details.objects.filter(email=email).exists():
      messages.info(request, 'Sorry, Email already exists')
      return redirect('registerstaff')
    else:
      
      staff=staff_details(first_name=fn,last_name=ln,email=email,user_name=un,contact=ph,password=pas,img=img,company=com)
      staff.save()
      return redirect('login')

  else:
    print(" error")
    return redirect('registerstaff')
  

  
def loginurl(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    passw = request.POST['pass']
    
    log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
    if log_user is not None:
      auth.login(request, log_user)
        
    if staff_details.objects.filter(user_name=user_name,password=passw,position='company').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='company') 

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
        return redirect('homepage')  

    if staff_details.objects.filter(user_name=user_name,password=passw,position='staff').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='staff')   

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
          return redirect('staffhome')  
    else:
      messages.info(request, 'Invalid Username or Password. Try Again.')
      return redirect('login')  
  else:  
   return redirect('login')   
  
def profile(request):
 
  return render(request, 'profile.html')
def purchase(request):
    if request.method == 'POST':
        customer_name = request.POST.get('cname')
        phone_number = request.POST.get('cno')
        billing_address = request.POST.get('billingAddress')
        bill_number = request.POST.get('bno')
        balance = request.POST.get('balance')
        bill_date = request.POST.get('bdate', timezone.now().strftime('%Y-%m-%d'))
        supply_source = request.POST.get('source')

        # Get the staff_id from the session
        staff_id = request.session.get('staff_id')

        try:
            staff = staff_details.objects.get(id=staff_id)
            company_id = staff.company_id
            party_names = Parties.objects.filter(company_id=company_id)
            customer = Parties.objects.get(party_name=customer_name)

            
            new_bill = FirstBill(
                customer=customer,
                bill_number=bill_number,
                bill_date=bill_date,
                supply_source=supply_source
            )
            new_bill.save()

           
            customer.phone_number = phone_number
            customer.billing_address = billing_address
            customer.opening_balance = balance
            customer.save()

            return render(request, 'purchasebill1.html', {'party_names': party_names})

        except staff_details.DoesNotExist:
          
            return redirect('login')

   
    staff_id = request.session.get('staff_id')
    company_id = staff_details.objects.get(id=staff_id).company_id
    party_names = Parties.objects.filter(company_id=company_id)
    return render(request, 'purchasebill1.html', {'party_names': party_names})
 


def first_page(request):
 
  return redirect('homepage')

def first_bill(request):
     if request.method == 'POST':
        customer_name = request.POST.get('cname')
        phone_number = request.POST.get('cno')
        billing_address = request.POST.get('billingAddress')
        bill_number = request.POST.get('bno')
        balance = request.POST.get('balance')
        bill_date = request.POST.get('bdate', timezone.now().strftime('%Y-%m-%d'))
        supply_source = request.POST.get('source')

       
        staff_id = request.session.get('staff_id')

        try:
            
            staff = staff_details.objects.get(id=staff_id)
            company_id = staff.company_id
            party_names = Parties.objects.filter(company_id=company_id)     
            customer = Parties.objects.get(party_name=customer_name)

           
            new_bill = FirstBill(
                customer=customer,
                bill_number=bill_number,
                bill_date=bill_date,
                supply_source=supply_source
            )
            new_bill.save()

            
            customer.phone_number = phone_number
            customer.billing_address = billing_address
            customer.opening_balance = balance
            customer.save()

            return render(request, 'first_bill.html', {'party_names': party_names})

        except staff_details.DoesNotExist:
            
            return redirect('login')

   
     staff_id = request.session.get('staff_id')
     company_id = staff_details.objects.get(id=staff_id).company_id
     party_names = Parties.objects.filter(company_id=company_id)
     return render(request, 'first_bill.html', {'party_names': party_names})
def add_purchase(request):
   
    if request.method == 'POST':
        customer_name = request.POST.get('cname')
        phone_number = request.POST.get('cno')
        billing_address = request.POST.get('billingAddress')
        bill_number = request.POST.get('bno')
        balance = request.POST.get('balance')
        bill_date = request.POST.get('bdate', timezone.now().strftime('%Y-%m-%d'))
        supply_source = request.POST.get('source')

        # Get the staff_id from the session
        staff_id = request.session.get('staff_id')

        try:
            staff = staff_details.objects.get(id=staff_id)
            company_id = staff.company_id
            party_names = Parties.objects.filter(company_id=company_id)
            customer = Parties.objects.get(party_name=customer_name)

            
            new_bill = FirstBill(
                customer=customer,
                bill_number=bill_number,
                bill_date=bill_date,
                supply_source=supply_source
            )
            new_bill.save()

           
            customer.phone_number = phone_number
            customer.billing_address = billing_address
            customer.opening_balance = balance
            customer.save()

            return render(request, 'add_purchase.html', {'party_names': party_names})

        except staff_details.DoesNotExist:
          
            return redirect('login')

   
    staff_id = request.session.get('staff_id')
    company_id = staff_details.objects.get(id=staff_id).company_id
    party_names = Parties.objects.filter(company_id=company_id)
    return render(request, 'add_purchase.html', {'party_names': party_names})
  
def get_items(request):
    # Replace 'company_id' and 'staff_id' with your actual model fields
    company_id = request.GET.get('company_id')
    staff_id = request.GET.get('staff_id')

    # Modify the filtering logic based on your actual model fields
    if company_id:
        items = ItemModel.objects.filter(company_id=company_id)
    elif staff_id:
        items = ItemModel.objects.filter(staff_id=staff_id)
    else:
        items = ItemModel.objects.all()

    item_list = [{'id': item.id, 'item_name': item.item_name} for item in items]
    return JsonResponse({'items': item_list})

def get_item_details(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)

        # Get the customer's state from the supply_source field
        customer_state = request.POST.get('source')  # Assuming 'source' is the field containing the state

        tax_rate = get_tax_rate(customer_state, item)

        item_details = {
            'hsn': item.item_hsn,
            'price': item.item_purchase_price,
            'tax_percent': tax_rate,
        }
        return JsonResponse(item_details)
    except ItemModel.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

def get_tax_rate(customer_state, item):
    # Implement the logic to determine tax rate based on customer's state and item's taxability
    # For example, you can have a dictionary mapping states to tax rates
    state_tax_rates = {
        'State1': 5,
        'State2': 8,
        # Add more states and tax rates as needed
    }

    default_tax_rate = 0  # Default tax rate if state not found in the dictionary

    # Replace 'StateX' with the actual state field in your ItemModel
    item_taxable = item.item_taxable

    # If item is taxable and the customer's state is in the dictionary, use that tax rate
    if item_taxable and customer_state in state_tax_rates:
        return state_tax_rates[customer_state]

    # Otherwise, return the default tax rate
    return default_tax_rate


def your_view_function(request):
    return render(request, 'purchasebill1.html')

def view_items(request):
    items = ItemModel.objects.all()
    return render(request, 'view_items.html', {'items': items})

def view_item_details(request, item_id):
    item = get_object_or_404(ItemModel, id=item_id)
    return render(request, 'view_item_details.html', {'item': item})

def edit_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemModel, id=item_id)
        item.item_name = request.POST.get('item_name')
        item.item_hsn = request.POST.get('item_hsn')
        item.item_purchase_price = request.POST.get('item_purchase_price')
        item.item_gst = request.POST.get('item_gst')
        item.item_igst = request.POST.get('item_igst')
        # Update other fields as needed
        item.save()
        return redirect('view_items')  # Redirect to the view_items page after editing
    else:
        item = get_object_or_404(ItemModel, id=item_id)
        return render(request, 'edit_item.html', {'item': item})
      
def add_item(request):
    if request.method == 'POST':
        # Process form data and create a new item
        # Extract data from the request.POST dictionary
        type = request.POST.get('type')
        name = request.POST.get('name')
        hsn = request.POST.get('hsn')
        unit = request.POST.get('unit')
        tax = request.POST.get('tax')
        sprice = request.POST.get('sprice', 0)
        pprice = request.POST.get('pprice', 0)
        gst = request.POST.get('gst', 0)
        igst = request.POST.get('igst', 0)
        sth = request.POST.get('sth')
        extraPrice = request.POST.get('extraPrice')
        date = request.POST.get('date')

        # Handle empty strings for numeric fields
        sprice = 0 if not sprice else sprice
        pprice = 0 if not pprice else pprice
        gst = 0 if not gst else gst
        igst = 0 if not igst else igst

        # Create a new ItemModel instance
        new_item = ItemModel.objects.create(
            item_name=name,
            item_hsn=hsn,
            item_unit=unit,
            item_taxable=tax,
            item_gst=gst,
            item_igst=igst,
            item_sale_price=sprice,
            item_purchase_price=pprice,
            item_stock_in_hand=sth,
            item_at_price=extraPrice,
            item_date=date,
            type=type
        )

        # Get all items to update the dropdown
        items = ItemModel.objects.values('id', 'item_name')

        # Return the newly created item and the updated dropdown
        return JsonResponse({'success': True, 'new_item': {'id': new_item.id, 'name': new_item.item_name}, 'items': list(items)})
    
    return render(request, 'purchasebill1.html.html')



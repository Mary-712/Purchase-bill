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
    # Replace this with your actual logic to fetch items
    items = ItemModel.objects.all()
    item_list = [{'id': item.id, 'item_name': item.item_name} for item in items]
    return JsonResponse({'items': item_list})
  
def get_item_details(request, item_id):
    item = ItemModel.objects.get(id=item_id)
    item_details = {
        'hsn': item.item_hsn,
        'price': item.item_purchase_price,
        'tax_percent': item.item_gst if item.item_taxable == 'GST' else item.item_igst,
    }
    return JsonResponse(item_details)

def your_view_function(request):
    return render(request, 'purchasebill1.html')

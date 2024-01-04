from . import views
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('service', views.service, name='service'),
    path('register', views.register, name='register'),
    path('registercompany', views.registercompany, name='registercompany'),
    path('registerstaff', views.registerstaff, name='registerstaff'),
    path('login', views.login, name='login'),
    path('registeruser', views.registeruser, name='registeruser'),
    path('add_company', views.add_company, name='add_company'),
    path('staff_registraction', views.staff_registraction, name='staff_registraction'),
    path('homepage', views.homepage, name='homepage'),
    path('staffhome', views.staffhome, name='staffhome'),
    path('loginurl', views.loginurl, name='loginurl'),
    path('logout', views.logout, name='logout'),
    path('base', views.base, name='base'),
    path('profile', views.profile, name='profile'),
    path('purchase', views.purchase, name='purchase'),
    path('add_purchase', views.add_purchase, name='add_purchase'),
    path('first_bill',views.first_bill,name='first_bill'),
    path('first_page',views.first_page,name='first_page'),
    path('get_item_details/<int:item_id>', views.get_item_details, name='get_item_details'),
    # path('add_purchase_bill',views.add_purchase_bill,name='add_purchase_bill'),
    # path('add_item', views.add_item, name='add_item'),
    path('get_items/', views.get_items, name='get_items'),
    path('get_item_details/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('your_view_path/', views.your_view_function, name='your_view_function'),
    path('items/', views.view_items, name='view_items'),
    path('items/<int:item_id>/', views.view_item_details, name='view_item_details'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('get_tax_rate',views.get_tax_rate,name='get_tax_rate'),
    path('add_item/', views.add_item, name='add_item'),
]
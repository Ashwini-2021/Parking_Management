from django.urls import path,include
from . import views
from .views import *
#from google import views as view

urlpatterns = [

    #homepage
    path('', views.HomePage,name='homepage'),
    path('contactUs/',views.hpContactUs,name='hpcontactus'),

    #Vehicle Owner
    path('voLogin/',views.voLogin,name='vologin'),
    path('voDesktop/',views.voDesktop,name='vodesktop'),
    path('voPayment/',views.voPayment,name='vopayment'),
    path('voHelp/',views.voHelp,name='vohelp'),
    path('voProfile/',views.voProfile,name='voprofile'),
    path('addVehicle/',views.addVehicle,name='addvehicle'),
    path('voLogout/',views.voLogout,name='vologout'),
    path('bookParking/<str:key>/<int:key1>',views.bookParking,name='bookparking'),
    path('unPark/',views.unPark,name='unpark'),
    path('parkingHistory/',views.parkingHistory,name='parkinghistory'),
    path('deleteVehicle/<str:key>',views.deleteVehicle,name='deletevehicle'),
    path('currentPS/',views.currentPS,name='currentps'),

    #Land Owner
    path('loLogin/',views.loLogin,name='lologin'),
    path('loHelp/',views.loHelp,name='lohelp'),
    path('loProfile/',views.loProfile,name='loprofile'),
    path('addPlace/',views.addPlace,name='addplace'),
    path('loLogout/',views.loLogout,name='lologout'),
    path('deletePlace/<str:key>',views.deletePlace,name='deleteplace'),
    path('loHelp/',views.loHelp,name='lohelp'),

    #Admin
    path('adminLogin/',views.aLogin,name='adminlogin'),
    path('adminDashboardLo/',views.adminDashboardLo,name='admindashboardlo'),
    path('adminDashboardvo/',views.adminDashboardvo,name='admindashboardvo'),
    path('admindashboard/',views.adminDashboard,name='admindashboard'),
    path('loDetails/',views.loDetails,name='lodetails'),
    path('deleteLO/<int:key>',views.deleteLO,name='deletelo'),
    path('voDetails/',views.voDetails,name='vodetails'),
    path('deleteVO/<int:key>',views.deleteVO,name='deletevo'),
    path('changeAdminPass/',views.changeAdminPass,name='changeadminpass'),
    path('pDetails/',views.pDetails,name='pdetails'),
    path('vDetails/',views.vDetails,name='vdetails'),
    path('lDetails/',views.lDetails,name='ldetails'),
    path('deleteV/<str:key>',views.deleteV,name='deletev'),
    path('deleteP/<int:key>',views.deleteP,name='deletep'),
    path('aLogout/',views.aLogout,name='alogout'),

]
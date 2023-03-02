from django.shortcuts import render,redirect
import mysql.connector as sql
from django.http import HttpResponse
from .models import VehicleDetails
import datetime
from django.contrib import messages 

#***********************************************************************************
#   Home Page Section
#***********************************************************************************
def HomePage(request):
    return render(request,'Park/HomePage.html')

username=''
email=''
subject=''
desc=''

def hpContactUs(request):
    global username,email,subject,desc

    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        try:
            data=request.POST
            for key,value in data.items():
                if key=="username":
                    username=value
                if key=="email":
                    email=value
                if key=="subject":
                    subject=value
                if key=="desc":
                    desc=value    

            query="insert into Help(UserName,EmailId,Subject,Description) values('%s','%s','%s','%s')" % (username,email,subject,desc)               
            cursor.execute(query)
            m.commit()  
            return render(request,'Park/HomePage.html')
                        
        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()
    return render(request,'Park/HomePageContactUS.html')  


#***********************************************************************************
#   Vehicle Owner Section
#***********************************************************************************
#creating global variables
username=''
email=''
phoneno=''
password1=''
password2=''
em=''
pass3=''
# Create your views here.
def voLogin(request): 
    global username,email,phoneno,password1,password2
    if request.method=="POST":
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        cursor1=m.cursor()
        
        #sign up form
        if request.POST.get("submit") == 'SignUp':
            data=request.POST
            for key,value in data.items():
                if key=="username":
                    username=value
                if key=="email":
                    email=value
                if key=="phoneno":
                    phoneno=value
                if key=="pass1":
                    password1=value
                if key=="pass2":
                    password2=value     

            c="insert into Vehicle_Owner_SignUp (VOusername,VOEmail,VOPhoneNo,Password) values('%s','%s','%s','%s')" % (username,email,phoneno,password1)               
            cursor.execute(c)
            m.commit()
            return redirect('vologin')  
        #Login form
        elif request.POST.get("submit") == 'Login':
            global em,pass3
            data=request.POST
            for key,value in data.items():
                if key=="email1":
                    em=value
                if key=="password3":
                    pass3=value   

            #q="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Vehicle_Owner_SignUp'"
            #cursor.execute(q)

            result = tuple(['Id','VOusername','VOEmail','VOPhoneNo','Password'])      
            
            c="select * from Vehicle_Owner_SignUp where VOEmail='{}' and Password= '{}'".format(em,pass3)                 
            cursor1.execute(c)
            t=tuple(cursor1.fetchall())
            res=''
            
            if t==():
                messages.error(request,"Incorrect Email or Password")
                return render(request,'Park/VehicleOwnerLogin.html')  
            else:
                res = dict(zip(result,t[0]))
                request.session['res']=res
                return redirect('vodesktop')  

    return render(request,'Park/VehicleOwnerLogin.html')  
 
def currentPS(request):
    if 'k' not in request.session:
        return render(request,'Park/VehicleOwnerDesktop1.html')
    
    return render(request,'Park/CurrentParkingStatus.html')
    
           

#defining global variables
VehicleType=''
VehicleCharges=''
Points=''
Vnum=''
def voDesktop(request):
    if 'res' not in request.session:
        return redirect('vologin')
    
    if 'k' in request.session:
        return redirect('bookparking')    

    #searching place for parking
    if request.method=='POST':
        global vtype,add,VehicleType,VehicleCharges,Points,Vnum
        try:
            m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
            cursor=m.cursor()
            data=request.POST

            for key,value in data.items():
                if key=="dropdown":
                    vtype=value
                if key=="place":
                    add=value       

            query="select * from Vehiclecharges where Vehicle_type='{}'".format(vtype) 
            cursor.execute(query)
            area=tuple(cursor.fetchall())
            area1=area[0][2]+50

            t=(vtype,add) 
            VehicleType=vtype
            VehicleCharges=int(area[0][3])
            Points=int(area[0][4])

            ses=request.session['res']
            id1=ses.get('Id')

            query2="select Vehicle_Number from vehicledetails where Vehicle_Type='{}' AND Id='{}'".format(vtype,id1)
            cursor.execute(query2)
            Vnum=cursor.fetchone()

            query1="select Place_Address,LO_username,Parking_Status,land_owner_signup.Id from land_owner_signup join landdetails on land_owner_signup.Id=landdetails.Id where landdetails.Place_address LIKE '%{}%' and landdetails.Place_Area BETWEEN '{}' AND '{}'".format(add,area[0][2],area1)     
            cursor.execute(query1)
            ans=tuple(cursor.fetchall())

            if ans==():
                return render(request,'Park/VehicleOwnerDesktop1.html',{'t':t})
            else:      
                return render(request,'Park/VehicleOwnerDesktop1.html',{'ans':ans,'t':t})

        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()

        return render(request,'Park/VehicleOwnerDesktop.html')    

    #taking vehicle type from vehicle owner
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        ses=request.session['res']
        id1=ses.get('Id')
              
        c="select Vehicle_Type from vehicledetails where Id='{}'".format(id1)               
        cursor.execute(c)
        vtype=tuple(cursor.fetchall())
   
        if vtype==():
            return render(request,'Park/VehicleOwnerDesktop.html')
        else:          
            return render(request,'Park/VehicleOwnerDesktop.html',{'vtype':vtype})

    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()

    return render(request,'Park/VehicleOwnerDesktop.html')  

def voProfile(request):
    m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
    cursor=m.cursor()

    ses=request.session['res']
    id1=ses.get('Id')
    #return HttpResponse(id1)

    c="select Vehicle_Type,Vehicle_Number from VehicleDetails where Id='{}'".format(id1)  
    cursor.execute(c)
    dat=tuple(cursor.fetchall())

    return render(request,'Park/VehicleOwnerProfile.html',{'dat':dat})     

def voPayment(request):
    return render(request,'Park/VehicleOwnerPaymentMethod.html')

def voHelp(request):
    global username,email,subject,desc
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        try:
            data=request.POST
            for key,value in data.items():
                if key=="username":
                    username=value
                if key=="email":
                    email=value
                if key=="subject":
                    subject=value
                if key=="desc":
                    desc=value    

            query="insert into Help(UserName,EmailId,Subject,Description) values('%s','%s','%s','%s')" % (username,email,subject,desc)               
            cursor.execute(query)
            m.commit()  
            return render(request,'Park/VehicleOwnerDesktop.html') 
                        
        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()
    
    return render(request,'Park/VehicleOwnerHelp.html')    

#******  Adding Vehicles to vehicle owners profile  *************#

vtype=''
vnum=''
add=''
def addVehicle(request):
    global vtype,vnum
    #return HttpResponse(request.method)
    if request.method=="POST":
       m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
       cursor=m.cursor()
        
       #extracting session data
       ses=request.session['res']
       id1=ses.get('Id')
       data=request.POST

       #return HttpResponse(data)
       for key,value in data.items():
           if key=="dropdown":
              vtype=value
           if key=="Vnum":
              vnum=value

       c="insert into VehicleDetails(Vehicle_Type,Vehicle_Number,Id) values('%s','%s','%s')" % (vtype,vnum,id1)               
       cursor.execute(c)
       m.commit()    

       return redirect('voprofile')   

    return render(request,'Park/VehicleDetails.html')  

def deleteVehicle(request,key):
       m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
       cursor=m.cursor()
        
       #extracting session data
       ses=request.session['res']
       id1=ses.get('Id')
       data=request.POST

       c="delete from VehicleDetails where Id='{}' AND Vehicle_Number='{}'".format(id1,key)               
       cursor.execute(c)
       m.commit()    

       return redirect('voprofile')


def voLogout(request):
    #if vehicle is parked then vehicle owner not logout from the app
    if 'k' in request.session:
        return render(request,'Park/CurrentParkingStatus.html')

    request.session.flush()
    return redirect('homepage')

#Booking a parking for vehicle
place_add=''
land_Id=''
ptime=''
uptime=''
def bookParking(request,key,key1):
    global place_add,land_Id,ptime

    if 'k' in request.session:
        return render(request,'VehicleOwnerDesktop1.html')
        
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()

        query1="select Points from land_owner_signup where Id='{}'".format(key1)
        cursor.execute(query1)
        pt=tuple(cursor.fetchall())
        pts=pt[0][0]+Points
        #return HttpResponse(pts)

        query2="update land_owner_signup set Points='{}' where Id='{}'".format(pts,key1) 
        cursor.execute(query2)
        m.commit() 

        query="update landdetails set Parking_Status='1' where Place_Address='{}' AND Id='{}'".format(key,key1) 
        cursor.execute(query)
        m.commit()

        #defining global variables
        place_add=key
        land_Id=key1
        ptime=datetime.datetime.now()

        k=(place_add,VehicleType,Vnum,VehicleCharges,Points)
        #return HttpResponse(k)
 
        request.session['k']=k
        #return HttpResponse(request.session['k'])
        return render(request,'Park/CurrentParkingStatus.html')   
                  
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
           cursor.close()
           m.close()

def unPark(request):
    global uptime

    if 'k' not in request.session:
        return redirect('bookparking')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
    
        query="update landdetails set Parking_Status='0' where Place_Address='{}' AND Id='{}'".format(place_add,land_Id) 
        cursor.execute(query)
        m.commit()   

        query1="select Income from admin"
        cursor.execute(query1)
        pt=tuple(cursor.fetchall())
        pts=pt[0][0]+request.session['k'][3]

        query2="update admin set Income='{}' where Id='{}'".format(pts,'1') 
        cursor.execute(query2)
        m.commit() 

        uptime=datetime.datetime.now()

        ses=request.session['res']
        id1=ses.get('Id')

        query3="Insert Into parkinghistory values('{}','{}','{}','{}','{}','{}','{}')".format(id1,ptime,uptime,place_add,request.session['k'][1],request.session['k'][2][0],request.session['k'][3])
        cursor.execute(query3)
        m.commit()

        del request.session['k']

        return render(request,'Park/VehicleOwnerPaymentMethod.html')   
                  
    except sql.Error as error:
        return HttpResponse("unsuccessful")
    finally:
        if m.is_connected():
           cursor.close()
           m.close()

def parkingHistory(request):
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()

        ses=request.session['res']
        id1=ses.get('Id')
    
        query="select * from parkinghistory where VId='{}'".format(id1) 
        cursor.execute(query)
        tup=tuple(cursor.fetchall()) 

        return render(request,'Park/ParkingHistory.html',{'tup':tup})   
                  
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
           cursor.close()
           m.close()           
    
#**************************************************************************************
#  Land Owners Section
#***************************************************************************************


def loLogin(request):
    global username,email,phoneno,password1,password2,em,pass3
    if request.method=="POST":
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        cursor1=m.cursor()
    
        if request.POST.get("submit") == 'SignUp':
            data=request.POST
            for key,value in data.items():
                if key=="username":
                    username=value
                if key=="email":
                    email=value
                if key=="phoneno":
                    phoneno=value
                if key=="pass1":
                    password1=value
                if key=="pass2":
                    password2=value     

            c="insert into Land_Owner_SignUp (LO_username,LO_Email,LO_PhoneNo,Password) values('%s','%s','%s','%s')" % (username,email,phoneno,password1)               
            cursor.execute(c)
            m.commit()
            return render(request,'Park/LandOwnerLogin.html')  

        #Login form
        elif request.POST.get("submit") == 'Login':
            global em,pass3
            data=request.POST
            for key,value in data.items():
                if key=="email1":
                    em=value
                if key=="password3":
                    pass3=value   
            
            #q="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Vehicle_Owner_SignUp'"
            #cursor.execute(q)

            result = tuple(['Id','LO_username','LO_Email','LO_PhoneNo','Password']) 

            c="select * from Land_Owner_SignUp where LO_Email='{}' and Password= '{}'".format(em,pass3)                 
            cursor1.execute(c)
            t=tuple(cursor1.fetchall())
            res = ''

            if t==():
                messages.error(request,"Incorrect Email or Password")
                return render(request,'Park/LandOwnerLogin.html')  
            else:
                res = dict(zip(result,t[0]))
                request.session['res']=res
                return redirect('loprofile')  

    return render(request,'Park/LandOwnerLogin.html') 

def loHelp(request):
    global username,email,subject,desc
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        try:
            data=request.POST
            for key,value in data.items():
                if key=="username":
                    username=value
                if key=="email":
                    email=value
                if key=="subject":
                    subject=value
                if key=="desc":
                    desc=value    

            query="insert into Help(UserName,EmailId,Subject,Description) values('%s','%s','%s','%s')" % (username,email,subject,desc)               
            cursor.execute(query)
            m.commit()  
            return render(request,'Park/LandOwnerProfile.html') 
                        
        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()
    
    return render(request,'Park/LandOwnerHelp.html')    

def loProfile(request):
    if 'res' not in request.session:
        return redirect('lologin')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()   
        
        #extracting session data
        ses=request.session['res']
        id1=ses.get('Id')    

        query1="select Points from land_owner_signup where Id='{}'".format(id1)  
        cursor.execute(query1)
        pts=tuple(cursor.fetchall())

        c="select Place_Address,Place_Area,image from LandDetails where Id='{}'".format(id1)                 
        cursor.execute(c)
        t=tuple(cursor.fetchall())

        return render(request,'Park/LandOwnerProfile.html',{'t':t,'pts':pts})
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
   
    return render(request,'Park/LandOwnerProfile.html')  

address=''
area=''
image=''
def addPlace(request):
    global address,area,image
    #return HttpResponse(request.method)
    if request.method=="POST":
        try:
            m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
            cursor=m.cursor()
            cursor1=m.cursor()
            #sign up form
            #return HttpResponse(request.POST.get("submit"))
            
            data=request.POST
            for key,value in data.items():
                if key=="add":
                    address=value
                if key=="area":
                    area=value
            image=request.FILES['img']   #important line    
                    
            #coverting image into binary file
            #with open(image,'rb') as f:
                 #picture=f.read()

            #extracting session data
            ses=request.session['res']
            id1=ses.get('Id')      

            c="insert into LandDetails(Place_Address,Place_Area,Image,Id) values('%s','%s','%s','%s')" % (address,area,image,id1)               
            cursor.execute(c)
            m.commit()
                
            return redirect('loprofile')
    
        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()

    return render(request,'Park/LandDetails.html')              

def loLogout(request):
    if 'res' in request.session:
        request.session.flush()
    return redirect('homepage')

def deletePlace(request,key):
    m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
    cursor=m.cursor()
        
    #extracting session data
    ses=request.session['res']
    id1=ses.get('Id')
    data=request.POST

    c="delete from landDetails where Id='{}' AND Place_Address='{}'".format(id1,key)               
    cursor.execute(c)
    m.commit()    

    return redirect('loprofile')


#***********************************************************************************
#   Admin Section
#***********************************************************************************

def aLogin(request):
    global em,pass3
    if request.method=="POST":
        try:
            m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
            cursor=m.cursor()
            
            data=request.POST
            for key,value in data.items():
                if key=="em":
                    em=value
                if key=="pass3":
                    pass3=value
        
            result = tuple(['Id','EmailId','Password']) 

            c="select * from Admin where EmailId='{}' and Password= '{}'".format(em,pass3)                 
            cursor.execute(c)
            t=tuple(cursor.fetchall())
            res = dict(zip(result,t))

            if t==():
                messages.error(request,"Incorrect Email or Password")
                return render(request,'Park/AdminLogin.html') 
            else:
                request.session['res']=res
                return redirect('admindashboard')
                
        except sql.Error as error:
            return HttpResponse(error)
        finally:
            if m.is_connected():
                cursor.close()
                m.close()

    return render(request,'Park/AdminLogin.html')  

def aLogout(request):
    if 'res' in request.session:
        request.session.flush()
    return redirect('homepage')   

def adminDashboardLo(request):
    return render(request,'Park/AdminDashboardLo.html')

def adminDashboardvo(request):
    return render(request,'Park/AdminDashboardvo.html')    

def adminDashboard(request):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()

        query1="select Income from admin where Id='{}'".format('1')
        cursor.execute(query1)
        t1=tuple(cursor.fetchall())

        query2="select count(VId) from parkinghistory"
        cursor.execute(query2)
        t2=tuple(cursor.fetchone())

        query3="select count(id1) from landdetails"
        cursor.execute(query3)
        t3=tuple(cursor.fetchone())

        query4="select count(Id) from vehicle_owner_signup"
        cursor.execute(query4)
        t4=tuple(cursor.fetchone())

        t=(t1,t2,t3,t4)

        return render(request,'Park/AdminDashboard.html',{'t':t})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()

    return render(request,'Park/AdminDashboard.html')

def loDetails(request):
    if 'res' not in request.session:
        return redirect('homepage')
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        c="select Id,LO_username,LO_Email,LO_PhoneNo from Land_Owner_SignUp"                 
        cursor.execute(c)
        t=tuple(cursor.fetchall())

        if t==():
            return redirect('admindashboardlo')  
        else:
            return render(request,'Park/AdminDashboardLo.html',{'t':t})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('admindashboard')

def deleteLO(request,key):
    if 'res' not in request.session:
        return redirect('homepage')
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        id=key

        c="delete from landdetails where Id='{}'".format(id)
        cursor.execute(c)
        m.commit()

        c="delete from Land_Owner_SignUp where Id='{}'".format(id)                 
        cursor.execute(c)
        m.commit()

        return redirect('lodetails')  
                        
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('lodetails')    

def voDetails(request):
    if 'res' not in request.session:
        return redirect('homepage')
    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        c="select Id,VOusername,VOEmail,VOPhoneNo from Vehicle_Owner_SignUp"                 
        cursor.execute(c)
        k=tuple(cursor.fetchall())

        if k==():
            return redirect('admindashboardvo')  
        else:
            return render(request,'Park/AdminDashboardvo.html',{'k':k})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('admindashboardvo')  

def deleteVO(request,key):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        id=key

        c="delete from vehicledetails where Id='{}'".format(id)
        cursor.execute(c)
        m.commit()

        c="delete from Vehicle_Owner_SignUp where Id='{}'".format(id)                 
        cursor.execute(c)
        m.commit()

        return redirect('vodetails')  
                        
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('vodetails')     

def changeAdminPass(request):
    return render(request,'Park/AdminDashboard.html')    

# all Parking place details
def lDetails(request):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        c="select * from landdetails"                 
        cursor.execute(c)
        k=tuple(cursor.fetchall())

        if k==():
            return redirect('ldetails') 
        else:
            return render(request,'Park/AdminDashboardLD.html',{'k':k})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('ldetails')
    
#total vehicle details
def vDetails(request):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        c="select * from Vehicledetails"                 
        cursor.execute(c)
        k=tuple(cursor.fetchall())

        if k==():
            return redirect('vdetails')  
        else:
            return render(request,'Park/AdminDashboardVD.html',{'k':k})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('vdetails')

#parking history of all users
def pDetails(request):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        
        c="select * from parkinghistory"                 
        cursor.execute(c)
        k=tuple(cursor.fetchall())

        if k==():
            return render(request,'Park/AdminDashboardHistory.html')  
        else:
            return render(request,'Park/AdminDashboardHistory.html',{'k':k})
                
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('admindashboardvo')

#remove parking place
def deleteP(request,key):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        id=key

        c="delete from landdetails where id1='{}'".format(id)
        cursor.execute(c)
        m.commit()

        return redirect('ldetails')  
                        
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return redirect('ldetails')

#remove vehicle 
def deleteV(request,key):
    if 'res' not in request.session:
        return redirect('homepage')

    try:
        m=sql.connect(host="localhost",user="root",passwd="",database="park_mentor_2")
        cursor=m.cursor()
        n=key

        c="delete from vehicledetails where Vehicle_Number='{}'".format(n)
        cursor.execute(c)
        m.commit()

        return redirect('vdetails')  
                        
    except sql.Error as error:
        return HttpResponse(error)
    finally:
        if m.is_connected():
            cursor.close()
            m.close()
    return render(request,'Park/AdminDashboard.html')   
      

     


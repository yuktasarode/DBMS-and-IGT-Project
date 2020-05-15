from django.shortcuts import render
from app.forms import RequestBloodForm
from basic_app.models import UserProfileInfo,Bloodbank,BloodCamps
from django.contrib.auth.models import User
from django.core.mail import send_mail
import folium
#from app.forms import DropForm
import datetime
from app.models import RequestBlood
from django.http import HttpResponse
from django.db.models import Q


# pls import database models

import dateutil

from django.http import JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
#User=get_user_model()

class HomeView(View):
    def get(selfself,request,*args,**kwargs):
        return render(request,'charts.html',{})




def get_data(request,*args,**kwargs):
    #return this dictionary
    data={
       "sales":100,
       "customer":10,
    }
    return JsonResponse(data)




class ChartData(APIView):
#models se data
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):


        # gender coloumn

        male=len(list(UserProfileInfo.objects.all().filter(Gender='M')))
        female=len(list(UserProfileInfo.objects.all().filter(Gender='F')))
        labels=['Male', 'Female']
        default_items=[male,female]


        labels2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June','July','Aug','Sep','Oct','Nov','Dec']
        campObject=list(BloodCamps.objects.all())
        times2 = []
        for ob in campObject:
            times2.append(ob.Organization_Date)

        CountJan=0
        CountFeb=0
        CountMar=0
        CountApr=0
        CountMay=0
        CountJune=0
        CountJuly=0
        CountAug=0
        CountSep=0
        CountOct=0
        CountNov=0
        CountDec=0
        for x in times2:
            monthNumber=x.month
            if monthNumber==1:
                CountJan+=1
            elif monthNumber==2:
                CountFeb+=1
            elif monthNumber==3:
                CountMar+=1
            elif monthNumber==4:
                CountApr+=1
            elif monthNumber==5:
                CountMay+=1
            elif monthNumber==6:
                CountJune+=1
            elif monthNumber==7:
                CountJuly+=1
            elif monthNumber==8:
                CountAug+=1
            elif monthNumber==9:
                CountSep+=1
            elif monthNumber==10:
                CountOct+=1
            elif monthNumber==11:
                CountNov+=1
            elif monthNumber==12:
                CountDec+=1


        default_items2 = [CountJan,CountFeb,CountMar,CountApr,CountMay,
                          CountJune,CountJuly,CountAug,CountSep,CountOct,CountNov,CountDec]
        data = {
            "labels": labels,
            "default": default_items,

            "labels2": labels2,
            "default2": default_items2,



        }
        return Response(data)
# Create your views here.
#def index(request):
#    return render(request,'index.html')

def about(request):
    return render(request,'aboutus2.html')

def bbmap(request):
    return render(request,'bbmap.html')

def citymap(request):
    return render(request,'show_city_map.html')

def showcitybb(request):
    return render(request,'show_city_bb.html')

def hmap(request):
    return render(request,'hospmap.html')

def dmap(request):
    return render(request,'dmap.html')

def feedback(request):
    return render(request,'Feedback2.html')


def reqblood(request):
    form= RequestBloodForm()
    name=''
    email=''
    contact_name=''
    contact_num=''
    hospital_name=''
    city=''
    date_of_requirement=''
    blood_group=''

    if request.method=="POST":
        form=RequestBloodForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            patient_name= form.cleaned_data.get("patient_name")
            email= form.cleaned_data.get("email")
            blood_group=form.cleaned_data.get("blood_group")
            contact_name=form.cleaned_data.get("contact_name")
            contact_num=form.cleaned_data.get("contact_num")
            city=form.cleaned_data.get("city")
            hospital_name=form.cleaned_data.get("hospital_name")
            date_of_requirement=form.cleaned_data.get("date_of_requirement")
            subject= "WingsOfLife: Somebody Needs Your Help"
            display=UserProfileInfo.objects.all().filter(City=city,Blood_group=blood_group)


            userids=[]
            rece=[]

            count = 0
            for bn in display:
                userids.append(display[count].user_id)
                count+=1

            for id in userids:
                disp=User.objects.get(id=id)
                rece.append(disp.email)


            comment=patient_name+" requires "+blood_group+" blood for treatment on "+str(date_of_requirement)+" at "+hospital_name+" , "+city+". You can contact "+contact_name+" at "+contact_num+" or email at " + email+". We at WingsOfLife request you to Donate Blood, Save Lives.Thank You!"
            send_mail(subject, comment, 'wingsoflifeofficial@gmail.com', rece)

            return HttpResponse("Your request has been saved.We hope to find a donor soon!")

    return render(request,'req_blood_form.html',{'form':form})

def drop(request):
    today = datetime.datetime.today()
    date_of_requirement =  datetime.datetime.today()
    items=RequestBlood.objects.all().filter(Q(date_of_requirement__gte=today)).order_by('date_of_requirement')
    city_items=RequestBlood.objects.all().distinct('city')
    blood_group_items=RequestBlood.objects.all().distinct('blood_group')
    #form= DropForm()
    detailsNotTaken=True
    city='Mumbai'
    blood_group='A+'
    display=RequestBlood.objects.all().filter(city=city,blood_group=blood_group)


    if request.method=="POST" and detailsNotTaken==True:
        city=request.POST.get('item_city')
        blood_group=request.POST.get('item_bg')
        detailsNotTaken=False

        try:
            if blood_group=="All":
                display=RequestBlood.objects.all().filter(city=city).filter(Q(date_of_requirement__gte=today)).order_by('date_of_requirement')
            elif city=="All":
                display=RequestBlood.objects.all().filter(Q(date_of_requirement__gte=today)).filter(blood_group=blood_group)
            else:
                display=RequestBlood.objects.all().filter(city=city,blood_group=blood_group).filter(Q(date_of_requirement__gte=today)).order_by('date_of_requirement')

            #item=UserProfileInfo.objects.all().filter(City=city)


        except RequestBlood.DoesNotExist:
            pass
    return render(request,'curr_req.html',{'itemc':city_items,'itembg':blood_group_items,'display':display,'detailsNotTaken':detailsNotTaken})

def cityreq(request):
    city_items=UserProfileInfo.objects.all().distinct('City')
    detailsNotTaken=True
    city='Mumbai'
    blood_group='A+'
    item=UserProfileInfo.objects.all().filter(City=city)
    blood_group_items=RequestBlood.objects.all().distinct('blood_group')

    if request.method=="POST" and detailsNotTaken==True:
        city=request.POST.get('item_city')
        blood_group=request.POST.get('item_bg')
        detailsNotTaken=False
        itemcount=1

        try:
            if blood_group=="All":
                item=UserProfileInfo.objects.all().filter(City=city)
            else:
                item=UserProfileInfo.objects.all().filter(City=city,Blood_group=blood_group)
                itemcount=UserProfileInfo.objects.all().filter(City=city,Blood_group=blood_group).count()
            lat=[]
            long=[]
            if itemcount>0:
                for it in item:
                    lat.append(it.latitude)
                    long.append(it.longitude)
                m=folium.Map(location=[lat[0],long[0]],zoom_start=12)

                for it in item:
                    tooltip="Blood Group:"+it.Blood_group+", Donations: "+str(it.No_of_donations)+" , Contact:"+it.Contact_No

                    folium.Marker([it.latitude,it.longitude],
                                   popup='<a href="https://www.google.com/maps/dir/?api=1">GetDirection</a>',

        tooltip=tooltip).add_to(m)


                m.save('templates/show_city_map.html')
                print(lat[0])
                print(long[0])

            else:
                return HttpResponse("No such Record found")


        except UserProfileInfo.DoesNotExist:
            pass
    return render(request,'citymap.html',{'itemc':city_items,'detailsNotTaken':detailsNotTaken,'itembg':blood_group_items})

def citybb(request):
        city_items=Bloodbank.objects.all().distinct('City')
        detailsNotTaken=True
        city='Mumbai'
        item=Bloodbank.objects.all().filter(City=city)

        if request.method=="POST" and detailsNotTaken==True:
            city=request.POST.get('item_city')
            detailsNotTaken=False

            try:
                item=Bloodbank.objects.all().filter(City=city)
                lat=[]
                long=[]
                for it in item:
                    lat.append(it.Latitude)
                    long.append(it.Longitude)
                m=folium.Map(location=[lat[0],long[0]],zoom_start=12)

                for it in item:
                    tooltip="Blood Bank:"+it.Blood_Bank_Name+" , Contact:"+it.Contact_No
                    url = "https://www.google.com/maps/dir/?api=1"
                    destination = "&destination=" + it.Latitude + "," + it.Longitude
                    newurl=url+destination
                    folium.Marker([it.Latitude,it.Longitude],
                                   popup='<a href="https://www.google.com/maps/dir/?api=1">GetDirection</a>',
                                   tooltip=tooltip).add_to(m)


                m.save('templates/show_city_bb.html')
                print(lat[0])
                print(long[0])
            except UserProfileInfo.DoesNotExist:
                pass
        return render(request,'citybb.html',{'itemc':city_items,'detailsNotTaken':detailsNotTaken,})







        #if form.is_valid():
        #    form.save(commit=True)
        #    return HttpResponse("Your request has been saved.We hope to find a donor soon!")

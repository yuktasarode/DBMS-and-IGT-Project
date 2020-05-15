from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm,UserForm,BloodBankForm,StockUpdateForm,CampsForm,EditProfileInfoForm
from basic_app.forms import UserProfileInfoForm,UserForm,BloodBankForm,CampsForm,EditProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from app.models import RequestBlood
from django.db.models import Q
import datetime
from django.contrib.auth import authenticate,login,logout
from .models import Bloodbank,UserProfileInfo,BloodCamps
from .models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,PasswordChangeForm
import csv
from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def userProfileInfoReport(request):
    """A view that streams a large CSV file."""
    if request.method=="POST":
        gender = request.POST.get('gender')
    model_class = UserProfileInfo
    print(gender)
    meta = model_class._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    if gender=='F' or gender=='M':
        for obj in model_class.objects.all().filter(Gender=gender):
            row = writer.writerow([getattr(obj, field) for field in field_names])
    else:
        for obj in model_class.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

def bloodBankReport(request):
    """A view that streams a large CSV file."""
    if request.method=="POST":
        state = request.POST.get('state')
    model_class = Bloodbank
    meta = model_class._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    if state=='All':
        for obj in model_class.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])
    else:
        for obj in model_class.objects.all().filter(State=state):
            row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

def campReport(request):
    """A view that streams a large CSV file."""
    if request.method=="POST":
        state = request.POST.get('state')
    model_class = BloodCamps
    meta = model_class._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    if state=='All':
        for obj in model_class.objects.all():
            row = writer.writerow([getattr(obj, field) for field in field_names])
    else:
        for obj in model_class.objects.all().filter(State=state):
            row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

def get_reports(request):
    return render(request,'basic_app/get_reports.html')


def index(request):
    bank=[]
    don=[]
    if request.user.is_anonymous:
        bank=[]
    else:
        bank = list(Bloodbank.objects.all().filter(user=request.user))
        don= list(UserProfileInfo.objects.all().filter(user=request.user))[0]

    userIsBank = False
    userIsdon=False
    if len(bank) > 0:
        userIsBank=True
    else:
        userIsBank=False
    



    aplus=UserProfileInfo.objects.all().filter(Blood_group='A+').count()
    bplus=UserProfileInfo.objects.all().filter(Blood_group='B+').count()
    amin=UserProfileInfo.objects.all().filter(Blood_group='A-').count()
    bmin=UserProfileInfo.objects.all().filter(Blood_group='B-').count()
    abplus=UserProfileInfo.objects.all().filter(Blood_group='AB+').count()
    abmin=UserProfileInfo.objects.all().filter(Blood_group='AB-').count()
    oplus=UserProfileInfo.objects.all().filter(Blood_group='O+').count()
    omin=UserProfileInfo.objects.all().filter(Blood_group='O-').count()

    today = datetime.datetime.today()
    bgovt=Bloodbank.objects.all().filter(Category='Government').count()
    bpri=Bloodbank.objects.all().filter(Category='Charity').count()
    req=RequestBlood.objects.all().filter(Q(date_of_requirement__gte=today)).count()
    camps=BloodCamps.objects.all().filter(Q(Organization_Date__gte=today)).count()
    return render(request,'index.html',{'userIsBank':userIsBank,'userIsdon':userIsdon,'don':don,'aplus':aplus,'bplus':bplus,'amin':amin,'bmin':bmin,'abmin':abmin,'abplus':abplus,'oplus':oplus,'omin':omin,'bgovt':bgovt,'bpri':bpri,'camps':camps,'req':req})



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))

def register(request):
    registered=False
    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                {'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("someone tried to login and failed")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("invalid login details ")
    else:
        return render(request,'basic_app/login.html',{})

def login_bloodbank(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("someone tried to login and failed")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("invalid login details")
    else:
        return render(request,'basic_app/login_bloodbank.html',{})

def bloodbank_home(request):
    bank = list(Bloodbank.objects.all().filter(user=request.user))[0]
    items=Stock.objects.all().filter(Bid=bank)
    return render(request,'basic_app/bloodbank_home.html',{'bank':bank,'items':items})

def editdetails(request):
    if request.method == 'POST':
        user_form = EditProfileInfoForm(request.POST,instance=request.user)
        city = request.POST.get('city')
        state = request.POST.get('state')
        district = request.POST.get('district')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')

        if user_form.is_valid():
            user_form.save()
            UserProfileInfo.objects.all().filter(user=request.user).update(City=city,State=state,District=district,Address=address,
                        Pincode=pincode,Contact_No=contact)
            print('Hello')
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors)
    else:
        user_form = EditProfileInfoForm(instance=request.user)

    return render(request, 'basic_app/editdetails.html', {'user_form':user_form})

def adddonations(request):
    if request.method=="POST":
        organizationdate = request.POST.get('organizationdate')
        organizationname = request.POST.get('organizationname')
        conductedby = request.POST.get('conductedby')
        organizationcontact = request.POST.get('organizationcontact')
        organizationdistrict = request.POST.get('organizationdistrict')
        code = request.POST.get('code')
        state = request.POST.get('state')
        district = request.POST.get('district')

        campObject=BloodCamps.objects.all().filter(Code=code)

        if not campObject:
            return HttpResponse("Invalid details. Please try again")
        else:
            print(campObject[0])
            no = UserProfileInfo.objects.get(user=request.user).No_of_donations
            no+=1
            print(no)
            UserProfileInfo.objects.all().filter(user=request.user).update(No_of_donations=no)
            return HttpResponse("Donation Updated")

    return render(request,'basic_app/adddonations.html')

def show_donations(request):
    user_profile = UserProfileInfo.objects.all().filter(user=request.user)
    getUser = user_profile[0]
    return render(request,'basic_app/show_donations.html',{'user':getUser})

def stock_availability(request):

    detailsNotTaken = True
    state= 'Andaman And Nicobar Islands'
    bloodgroup='AB+'
    bloodcomponent='WB'
    itemst=Bloodbank.objects.all().distinct('State')
    itembg=Stock.objects.all().distinct('Blood_group')


    bank = Bloodbank.objects.all().filter(State=state)
    arrayOfStock = []
    arrOfBids = []
    join=[]

    if(request.method=="POST") and detailsNotTaken!=False:
        state = request.POST.get('state')
        bloodgroup = request.POST.get('bloodgroup')
        bloodcomponent = request.POST.get('bloodcomponent')
        detailsNotTaken = False


        bank = Bloodbank.objects.all().filter(State=state)
        count = 0
        for bn in bank:
            arrOfBids.append(bank[count].id)
            count+=1

        for id in arrOfBids:
            arrayOfStock.append(Stock.objects.all().filter(Blood_component=bloodcomponent,
                                                Blood_group=bloodgroup,Bid_id=id).select_related('Bid')[0])

        #print(arrOfBids)
        print("{} {} {}".format(state,bloodgroup,bloodcomponent))
        #print(arrayOfStock)
        #bplus=UserProfileInfo.objects.all().filter(Blood_group='B+').count()
        join=Stock.objects.all().filter(Blood_component=bloodcomponent,
                                            Blood_group=bloodgroup).select_related('Bid')

        #print(join)
    return render(request,'basic_app/stock_availability.html',{'join':join,'stock':arrayOfStock,'bank':bank,'itembg':itembg,'itemst':itemst,'detailsNotTaken':detailsNotTaken})




def updatestock(request):
    bloodgroup = 'AB'
    bloodcomponent = 'XY'

    if request.method=="POST":
        bloodgroup = request.POST.get('bloodgroup')
        bloodcomponent = request.POST.get('bloodcomponent')
        bags = request.POST.get('bags')
        cost = request.POST.get('cost')
        datetime = request.POST.get('datetime')
        bankName = list(Bloodbank.objects.all().filter(user=request.user))[0]

        Stock.objects.filter(
            Blood_component=bloodcomponent,
            Blood_group=bloodgroup,
            Bid=bankName).update(Number_of_bags=bags,Cost=cost,Last_updated=datetime)

    return render(request,'basic_app/updatestock.html',{'user':request.user})

def camps(request):
    detailsNotTaken = True
    state= 'Andaman And Nicobar Islands'
    orgby="All"
    #district='Ahmedabad'
    camp = BloodCamps.objects.all().filter(State=state)
    today = datetime.datetime.today()
    items=BloodCamps.objects.all().distinct('Organization_Name')


    if(request.method=="POST") and detailsNotTaken!=False:
        state = request.POST.get('state')
        orgby=request.POST.get('orgby')
        #district = request.POST.get('district')
        detailsNotTaken = False

        try:
            if orgby=="All":
                camp = BloodCamps.objects.all().filter(Q(Organization_Date__gte=today)).filter(State=state).order_by('District')
            else:
                camp = BloodCamps.objects.all().filter(Q(Organization_Date__gte=today)).filter(State=state,Organization_Name=orgby).order_by('District')
        except BloodCamps.DoesNotExist:
            pass
        print("{} ".format(state))
        print(orgby)
        print(camp)

    return render(request,'basic_app/camps.html',{'camp':camp,'detailsNotTaken':detailsNotTaken,'items':items})

def change_password(request):
    if request.method=="POST":
        form = PasswordChangeForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PasswordChangeForm()

        return render(request,'basic_app/change_password.html',{form:'form'})

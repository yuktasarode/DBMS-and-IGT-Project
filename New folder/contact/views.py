from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail

def contactview(request):
    name=''
    email=''
    comment=''


    form= ContactForm(request.POST or None)
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")
        subject= "A Visitor's Comment"


        comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, 'wingsoflifeofficial@gmail.com', ['wingsoflifeofficial@gmail.com',])

        return HttpResponse('Thank you for contacting us. We will get back to you soon!')
        #context= {'form': form}
        #return render(request, 'contact.html', context)

    else:
        context= {'form': form}
        return render(request, 'contact.html', context)


# Create your views here.

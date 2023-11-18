from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm
from django.contrib import messages

def home(request):
    return render(request, 'website/index.html')
def about(request):
    return render(request, 'website/about.html')
def services(request):
    return render(request, 'website/services-details.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print("POST request received")
        if form.is_valid():
            print("Form is valid")
            contact = form.save(commit=False)
            contact.name = 'Anonymous'
            contact.save()
            messages.success(request, 'Submitted correctly')
            return HttpResponseRedirect('/contact')
        else:
            print("Form is invalid")
            messages.error(request, 'shet!!!!!!!')
            print(form.errors)
    else:
        form = ContactForm()

    print("Rendering the contact.html template")
    return render(request, 'website/contact.html', {'form': form})


# def newsletter(request):
#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Sent !')
#             return HttpResponseRedirect('/')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.add_message(request, messages.ERROR, f"Form error for field {field}: {error}")
#     else:
#         form = NewsletterForm()

#     return HttpResponseRedirect('/')



def coming_soon(request):
    return render(request, 'coming_soon.html')
from django.shortcuts import render

# Create your views here.

def portfolio(request):
    return render(request, 'portfolio/portfolio.html')
    

def portfolio_details(request):
    return render(request, 'portfolio/portfolio-details.html')
    
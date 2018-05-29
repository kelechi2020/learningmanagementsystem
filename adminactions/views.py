from django.shortcuts import render

# Create your views here.


def admin_landing_page(request):
    return render(request, 'externals/admin_dashboard.html')
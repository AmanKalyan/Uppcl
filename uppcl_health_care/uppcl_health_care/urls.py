from django.contrib import admin
from django.urls import path, include
from user_management_app.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', home, name='home'),  # Root URL redirects to login
    path('', include('user_management_app.urls')),  # Include the user_management_app URLs
    path('reimbursement/', include('medical_reimbursement_app.urls')),  # Other app URLs
    path('cashless/', include('medical_cashless_treatment.urls')),
    path('advance/', include('medical_advance_treatment.urls')),
]

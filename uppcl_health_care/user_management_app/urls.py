from django.urls import path
from . import views

urlpatterns = [
    #path('',views.home,name='home'), #home page view
    path('', views.user_login, name='user_login'),  # Login page
    path('logout/', views.user_logout, name='user_logout'),  # Logout page
    path('signup/', views.user_signup, name='user_signup'),  # Signup page
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/add_details/', views.add_details, name='add_details'),
   
    # path('profile/', views.profile_management, name='profile_management'),  # Profile management
    path('reimbursement-selection/', views.reimbursement_selection, name='reimbursement_selection'),
]

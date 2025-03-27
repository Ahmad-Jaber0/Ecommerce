from django.urls import path
from account.views.auth_views  import register,current_user,update_user
from account.views.password_reset_views import forgot_password,reset_password

urlpatterns = [
    path('register/',register,name='register'),
    path('user/', current_user, name='user-data'),
    path('user/update/', update_user,name='update_user'), 
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/', reset_password, name='reset_password'),
]

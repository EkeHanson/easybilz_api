from django.urls import path
from . import views

urlpatterns = [

    path('send-registration-email/', views.send_registration_email, name='send_registration_email'),
    
    path('contact_admin_email/', views.contact_admin_email, name='send_registration_email'),

    path('create/', views.CreateUserAPIView.as_view(), name='create_user'),

    path('create/<int:pk>/', views.UserDetailAPIView.as_view(), name='edit_user'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('password/reset/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

     path('send-email/', views.send_email, name='send_email'),
]

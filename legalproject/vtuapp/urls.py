
from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordChangeView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.SignUp.as_view(), name='register'),
    # path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/',login_required(views.PasswordChangeView.as_view(template_name='registration/password_change_form.html')), name='password-change'),
    path('change-password-done/', views.password_success, name='password_success'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('profile/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    # path('update-user-profile/<int:pk>/', views.UpdateUserProfile.as_view(), name='user_profile_update'),
    
    # Reset password urls
    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
    
    
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
   
]


admin.site.site_title = "LegitData"
admin.site.site_header = "Welcome To LegitData Admin Panel"

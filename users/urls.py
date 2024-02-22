from django.urls import path
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users import views as custom_views
app_name = UsersConfig.name

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', custom_views.RegisterView.as_view(), name='register'),
    path('profile/', custom_views.ProfileView.as_view(), name='profile'),
    path('confirm_email/<int:pk>', custom_views.ConfirmPage.as_view(), name='confirm_email'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   ]




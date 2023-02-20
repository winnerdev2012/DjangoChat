from django.urls import path
from django.contrib.auth import views as auth_views
from authenticate.views import CustomLoginView, CustomLogoutView, CustomSignUpView

app_name = "authenticate"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name=""), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name=""), name='password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('signup/', CustomSignUpView.as_view(), name='signup')
]
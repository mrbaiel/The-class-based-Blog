from django.urls import path

from apps.accounts import views
from apps.accounts.views import ProfileUpdateView, ProfileDetailView, UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name = 'profile_edit'),
    path('user/<slug:slug>/', ProfileDetailView.as_view(), name = 'profile_detail'),
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
 ]

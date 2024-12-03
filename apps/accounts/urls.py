from django.urls import path

from apps.accounts import views
from apps.accounts.views import ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name = 'profile_edit'),
    path('user/<slug:slug>/', ProfileDetailView.as_view(), name = 'profile_detail'),
 ]

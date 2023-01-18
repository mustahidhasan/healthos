from django.conf import settings
from django.urls import path
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import AddPlan, CanclePlan, AddDataPlan
urlpatterns = [
    path('cancle/plan/', CanclePlan.as_view()),
    path('add/plan/', AddPlan.as_view()),
    path('add/data/plan/', AddDataPlan.as_view()),


]

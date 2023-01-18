from django.urls import path

from .views import  * 

urlpatterns = [
    path('config/', StipConfig.as_view()),
    path('create/checkout/session/', CreateCheckoutSession.as_view()),
    # path('webhook/', StripeWebHook.as_view()),
]

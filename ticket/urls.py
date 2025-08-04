from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('private/event',PrivateEventVeiwSet,basename='private')
router.register('public/event',PublicEventViewSet,basename='public')
router.register('private/ticket',TicketViewSet,basename='ticket')

urlpatterns = [
    path('register/',RegisterApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('',include(router.urls)),
    path('booking/',BookingViewSet.as_view())
]
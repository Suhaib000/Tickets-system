from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, AgentTicketViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='tickets')

urlpatterns = [
    path('', include(router.urls)),
    path('agent/tickets/', AgentTicketViewSet.as_view({'get': 'fetch_tickets'}), name='fetch-tickets'),
]

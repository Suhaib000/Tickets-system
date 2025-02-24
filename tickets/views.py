from rest_framework import viewsets, permissions, status
from .models import Ticket
from .serializers import TicketSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

User = get_user_model()

class TicketViewSet(viewsets.ModelViewSet):
    """
    Admin can Create, Update, and Delete tickets.
    """
    queryset = Ticket.objects.all().order_by('created_at')
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]



class AgentTicketViewSet(viewsets.ViewSet):
    """
    Agents can fetch and assign unassigned tickets.
    """
    permission_classes = [permissions.IsAuthenticated]

        
    @action(detail=False, methods=['get'])
    def fetch_tickets(self, request):
        MAX_TICKETS_PER_AGENT = 15
        agent = request.user

        # Ensure the user is an agent
        if agent.role != 'agent':
            return Response({"error": "Only agents can fetch tickets."}, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():  # Ensure safe concurrent updates
            
            # Check how many tickets are already assigned to this agent
            assigned_tickets = Ticket.objects.filter(assigned_agent=agent, status='assigned')
            current_assigned_count = assigned_tickets.count()
            count = MAX_TICKETS_PER_AGENT - current_assigned_count

            if count <= 0:
                # Agent already has 15 tickets, return their assigned tickets
                serializer = TicketSerializer(assigned_tickets, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Retrieve unassigned ticket IDs (ensuring safe slicing)
            unassigned_ticket_ids = list(
                Ticket.objects.filter(status='unassigned')
                .order_by('created_at')  # Ensure tickets are fetched in creation order
                .select_for_update(skip_locked=True)  # Lock rows to prevent race conditions
                .values_list('id', flat=True)[:count]
            )

            if unassigned_ticket_ids:
                # Assign these tickets to the agent
                Ticket.objects.filter(id__in=unassigned_ticket_ids).update(assigned_agent=agent, status='assigned')

            # Fetch updated assigned tickets for the agent
            all_tickets = Ticket.objects.filter(assigned_agent=agent, status='assigned')

        return Response(TicketSerializer(all_tickets, many=True).data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['post'])
    def sell_ticket(self, request, pk=None):
        agent = request.user
        try:
            ticket = Ticket.objects.get(id=pk, assigned_agent=agent)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found or not assigned to you."}, status=status.HTTP_403_FORBIDDEN)

        # Mark ticket as sold
        ticket.status = 'sold'
        ticket.save()

        return Response({"message": "Ticket sold successfully!"}, status=status.HTTP_200_OK)
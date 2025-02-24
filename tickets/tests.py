from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Ticket

User = get_user_model()

class TicketAPITest(APITestCase):
    def setUp(self):
        """
        Create test users (Admin & Agents) and sample tickets.
        """
        # Create an admin user
        self.admin = User.objects.create_user(username="admin", password="adminpass", role="admin")

        # Create two agent users
        self.agent1 = User.objects.create_user(username="agent1", password="agentpass", role="agent")
        self.agent2 = User.objects.create_user(username="agent2", password="agentpass", role="agent")

        # Create 20 unassigned tickets
        self.tickets = [Ticket.objects.create(title=f"Ticket {i}", status='unassigned') for i in range(20)]

        # Setup API clients for authentication
        self.admin_client = APIClient()
        self.agent1_client = APIClient()
        self.agent2_client = APIClient()

        self.admin_client.force_authenticate(user=self.admin)
        self.agent1_client.force_authenticate(user=self.agent1)
        self.agent2_client.force_authenticate(user=self.agent2)


    def test_agent_fetches_15_tickets(self):
        """
        Ensure an agent receives 15 tickets when fetching.
        """
        response = self.agent1_client.get('/agent/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 15)

        # Check if tickets are correctly assigned
        assigned_tickets = Ticket.objects.filter(assigned_agent=self.agent1)
        self.assertEqual(assigned_tickets.count(), 15)

    def test_agent_fetches_15_tickets(self):
        """
        Ensure an agent receives 15 tickets when fetching.
        """
        response = self.agent1_client.get('/agent/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 15)

        # Check if tickets are correctly assigned
        assigned_tickets = Ticket.objects.filter(assigned_agent=self.agent1)
        self.assertEqual(assigned_tickets.count(), 15)

    def test_agent_cannot_have_more_than_15_tickets(self):
        """
        Ensure an agent does not get more than 15 tickets.
        """
        # First fetch (assigns 15)
        self.agent1_client.get('/agent/tickets/')

        # Second fetch should return the same 15, not more
        response = self.agent1_client.get('/agent/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 15)

    def test_agents_get_different_tickets(self):
        """
        Ensure two agents do not receive the same ticket.
        """
        response1 = self.agent1_client.get('/agent/tickets/')
        response2 = self.agent2_client.get('/agent/tickets/')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Get assigned ticket IDs
        agent1_ticket_ids = {ticket["id"] for ticket in response1.data}
        agent2_ticket_ids = {ticket["id"] for ticket in response2.data}

        # Ensure no overlap
        self.assertTrue(agent1_ticket_ids.isdisjoint(agent2_ticket_ids))
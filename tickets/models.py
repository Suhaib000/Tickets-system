from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('sold', 'Sold'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'agent'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unassigned')

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

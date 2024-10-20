from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)  # Optional field to provide additional info about the skill

    def __str__(self):
        return self.name
    
class Trade(models.Model):
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='initiated_trades', on_delete=models.CASCADE)
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='responded_trades', on_delete=models.CASCADE, null=True, blank=True)
    initiator_skills = models.ManyToManyField(Skill, related_name='initiator_skill_trades')
    responder_skills = models.ManyToManyField(Skill, related_name='responder_skill_trades', blank=True)
    desired_skills = models.ManyToManyField(Skill, related_name='desired_skill_trades', blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    initiator_terms = models.TextField(blank=True)  # Terms offered by the initiator
    responder_terms = models.TextField(blank=True)  # Terms countered by the responder
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # Set when trade is completed
    title = models.CharField(max_length=255, blank=True, null=True)  # Title of the trade
    description = models.TextField(blank=True, null=True)  # Description of the trade

    def __str__(self):
        return f"Trade between {self.initiator} and {self.responder}"
    
    

class Queue(models.Model):
    trade = models.ForeignKey(Trade, related_name='queue', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trade_queue', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Applied', 'Applied'),
        ('Invited', 'Invited'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ], default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    invited_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Queue for trade {self.trade.id} by user {self.user.username}"

class Review(models.Model):
    trade = models.OneToOneField(Trade, related_name='review', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_given', on_delete=models.CASCADE)
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username}"

class Message(models.Model):
    trade = models.ForeignKey(Trade, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages_trade', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages_trade', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} in trade {self.trade.id}"

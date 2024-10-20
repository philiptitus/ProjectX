from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),#
    path('new/', CreateTradeView.as_view(), name='new-trade'),#
    path('add-skill/', AddSkillView.as_view(), name='add-skill'),#
    path('remove-skill/', RemoveSkillView.as_view(), name='remove-skill'),#
    path('apply/', ApplyToTradeView.as_view(), name='apply-to-trade'),#
    path('invite/', InviteToTradeView.as_view(), name='invite-to-trade'),#
    path('respond-to-invitation/', RespondToInvitationView.as_view(), name='respond-to-invitation'),#
    path('accept/', AcceptApplicationView.as_view(), name='accept-application'),#
    path('remove-from-trade/', RemoveFromTradeView.as_view(), name='remove-from-trade'),
    path('remove-self-from-trade/', RemoveSelfFromTradeView.as_view(), name='remove-self-from-trade'),
    path('complete-trade/', CompleteTradeView.as_view(), name='complete-trade'),
    path('create-message/', CreateMessageView.as_view(), name='create-message'),
    path('list-messages/', ListMessagesView.as_view(), name='list-messages'),
    path('delete-message/', DeleteMessageView.as_view(), name='delete-message'),
    path('create-review/', CreateReviewView.as_view(), name='create-review'),
    path('update-review/', UpdateReviewView.as_view(), name='update-review'),
    path('delete-review/', DeleteReviewView.as_view(), name='delete-review'),
    path('list-reviews/', ListReviewsView.as_view(), name='list-reviews'),
    path('trades/', TradeListView.as_view(), name='trade-list'),
    path('trades/<int:pk>/', TradeDetailView.as_view(), name='trade-detail'),
    path('trades/<int:trade_id>/queues/', QueueListView.as_view(), name='queue-list'),

]

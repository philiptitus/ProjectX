from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import SkillSerializer, TradeSerializer, QueueSerializer, QueueResponseSerializer, MessageSerializer, ReviewSerializer
from base.models import *
from django.utils import timezone

from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from base.serializers import *


class AddSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        skill_id = request.data.get('skill_id')

        if not skill_id:
            return Response({"error": "Skill ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response({"error": "Skill does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user.skills_offered.count() >= 10:
            return Response({"error": "You cannot add more than 10 skills."}, status=status.HTTP_400_BAD_REQUEST)

        if user.skills_offered.filter(id=skill.id).exists():
            return Response({"error": "You have already added this skill."}, status=status.HTTP_400_BAD_REQUEST)

        user.skills_offered.add(skill)
        user.save()

        return Response({"message": f"Skill '{skill.name}' added successfully."}, status=status.HTTP_201_CREATED)



class RemoveSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        skill_id = request.data.get('skill_id')

        if not skill_id:
            return Response({"error": "Skill ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response({"error": "Skill does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.skills_offered.filter(id=skill.id).exists():
            return Response({"error": "You do not have this skill in your profile."}, status=status.HTTP_400_BAD_REQUEST)

        user.skills_offered.remove(skill)
        user.save()

        return Response({"message": f"Skill '{skill.name}' removed successfully."}, status=status.HTTP_200_OK)

class CreateTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Validate the input data
        serializer = TradeSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the initiator skills from the user's skills
        initiator_skills = data.get('initiator_skills', [])
        if not initiator_skills:
            return Response({"error": "Initiator skills are required."}, status=status.HTTP_400_BAD_REQUEST)

        for skill_id in initiator_skills:
            try:
                skill = Skill.objects.get(id=skill_id)
            except Skill.DoesNotExist:
                return Response({"error": f"Skill with ID {skill_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.skills_offered.filter(id=skill.id).exists():
                return Response({"error": f"You do not have the skill with ID {skill_id} in your profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the desired skills
        desired_skills = data.get('desired_skills', [])
        for skill_id in desired_skills:
            try:
                skill = Skill.objects.get(id=skill_id)
            except Skill.DoesNotExist:
                return Response({"error": f"Desired skill with ID {skill_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the trade object
        trade = Trade.objects.create(
            initiator=user,
            title=data.get('title'),
            description=data.get('description'),
            initiator_terms=data.get('initiator_terms'),
            status='Pending'
        )

        # Add the initiator skills to the trade
        for skill_id in initiator_skills:
            skill = Skill.objects.get(id=skill_id)
            trade.initiator_skills.add(skill)

        # Add the desired skills to the trade
        for skill_id in desired_skills:
            skill = Skill.objects.get(id=skill_id)
            trade.desired_skills.add(skill)

        # Serialize the created trade object
        trade_serializer = TradeSerializer(trade)
        return Response(trade_serializer.data, status=status.HTTP_201_CREATED)



class ApplyToTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        trade_id = request.data.get('trade_id')

        if not trade_id:
            return Response({"error": "Trade ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has the required skills
        desired_skills = trade.desired_skills.all()
        user_skills = user.skills_offered.all()

        missing_skills = desired_skills.difference(user_skills)
        if missing_skills.exists():
            missing_skill_names = [skill.name for skill in missing_skills]
            return Response({"error": f"You do not have the required skills: {', '.join(missing_skill_names)}."}, status=status.HTTP_400_BAD_REQUEST)

        if Queue.objects.filter(trade=trade, user=user).exists():
            return Response({"error": "You have already applied to this trade."}, status=status.HTTP_400_BAD_REQUEST)

        queue_entry = Queue.objects.create(trade=trade, user=user, status='Applied')

        serializer = QueueSerializer(queue_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime  # Import datetime module
from .serializers import QueueSerializer

class InviteToTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        initiator = request.user
        trade_id = request.data.get('trade_id')
        invitee_id = request.data.get('invitee_id')

        if not trade_id or not invitee_id:
            return Response({"error": "Trade ID and Invitee ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id, initiator=initiator)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist or you are not the initiator."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitee = CustomUser.objects.get(id=invitee_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invitee does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the invitee has the required skills
        desired_skills = trade.desired_skills.all()
        invitee_skills = invitee.skills_offered.all()

        missing_skills = desired_skills.difference(invitee_skills)
        if missing_skills.exists():
            missing_skill_names = [skill.name for skill in missing_skills]
            return Response({"error": f"The invitee does not have the required skills: {', '.join(missing_skill_names)}."}, status=status.HTTP_400_BAD_REQUEST)

        if Queue.objects.filter(trade=trade, user=invitee).exists():
            return Response({"error": "This user has already been invited or applied to this trade."}, status=status.HTTP_400_BAD_REQUEST)

        queue_entry = Queue.objects.create(trade=trade, user=invitee, status='Invited', invited_at=datetime.now())

        serializer = QueueSerializer(queue_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RespondToInvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        queue_id = request.data.get('queue_id')
        action = request.data.get('action')  # 'accept' or 'decline'
        responder_terms = request.data.get('responder_terms')

        if not queue_id or not action:
            return Response({"error": "Queue ID and action are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queue_entry = Queue.objects.get(id=queue_id, user=user)
        except Queue.DoesNotExist:
            return Response({"error": "Queue entry does not exist or you are not the invitee."}, status=status.HTTP_400_BAD_REQUEST)

        trade = queue_entry.trade

        if action == 'accept':
            if not responder_terms:
                return Response({"error": "Responder terms are required for acceptance."}, status=status.HTTP_400_BAD_REQUEST)

            responder_skills = user.skills_offered.all()

            trade.responder = user
            trade.responder_terms = responder_terms
            trade.status = 'Accepted'
            trade.save()

            trade.responder_skills.set(responder_skills)

            queue_entry.status = 'Accepted'
            queue_entry.accepted_at = datetime.now()
            queue_entry.save()

            Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()
        elif action == 'decline':
            queue_entry.status = 'Rejected'
            queue_entry.rejected_at = datetime.now()
            queue_entry.save()

            Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        initiator = request.user
        queue_id = request.data.get('queue_id')
        action = request.data.get('action')  # 'accept' or 'decline'
        responder_terms = request.data.get('responder_terms')

        if not queue_id or not action:
            return Response({"error": "Queue ID and action are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queue_entry = Queue.objects.get(id=queue_id)
        except Queue.DoesNotExist:
            return Response({"error": "Queue entry does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        trade = queue_entry.trade

        if trade.initiator != initiator:
            return Response({"error": "You are not the initiator of this trade."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'accept':
            if not responder_terms:
                return Response({"error": "Responder terms are required for acceptance."}, status=status.HTTP_400_BAD_REQUEST)

            responder = queue_entry.user
            responder_skills = responder.skills_offered.all()

            trade.responder = responder
            trade.responder_terms = responder_terms
            trade.status = 'Accepted'
            trade.save()

            trade.responder_skills.set(responder_skills)

            queue_entry.status = 'Accepted'
            queue_entry.accepted_at = datetime.now()
            queue_entry.save()

            Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()
        elif action == 'decline':
            queue_entry.status = 'Rejected'
            queue_entry.rejected_at = datetime.now()
            queue_entry.save()

            Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RemoveFromTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        initiator = request.user
        queue_id = request.data.get('queue_id')

        if not queue_id:
            return Response({"error": "Queue ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queue_entry = Queue.objects.get(id=queue_id)
        except Queue.DoesNotExist:
            return Response({"error": "Queue entry does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        trade = queue_entry.trade

        if trade.initiator != initiator:
            return Response({"error": "You are not the initiator of this trade."}, status=status.HTTP_400_BAD_REQUEST)

        queue_entry.status = 'Rejected'
        queue_entry.rejected_at = timezone.now()
        queue_entry.save()

        Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()

        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveSelfFromTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        queue_id = request.data.get('queue_id')

        if not queue_id:
            return Response({"error": "Queue ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queue_entry = Queue.objects.get(id=queue_id, user=user)
        except Queue.DoesNotExist:
            return Response({"error": "Queue entry does not exist or you are not the user in the queue."}, status=status.HTTP_400_BAD_REQUEST)

        trade = queue_entry.trade

        queue_entry.status = 'Rejected'
        queue_entry.rejected_at = timezone.now()
        queue_entry.save()

        Queue.objects.filter(trade=trade).exclude(id=queue_entry.id).delete()

        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompleteTradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        initiator = request.user
        trade_id = request.data.get('trade_id')

        if not trade_id:
            return Response({"error": "Trade ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if trade.initiator != initiator:
            return Response({"error": "You are not the initiator of this trade."}, status=status.HTTP_400_BAD_REQUEST)

        if trade.status != 'Accepted':
            return Response({"error": "Trade must be accepted before it can be completed."}, status=status.HTTP_400_BAD_REQUEST)

        trade.status = 'Completed'
        trade.completed_at = timezone.now()
        trade.save()

        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        trade_id = request.data.get('trade_id')
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        if not trade_id or not receiver_id or not content:
            return Response({"error": "Trade ID, receiver ID, and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if trade.status not in ['Accepted', 'In Progress']:
            return Response({"error": "Trade is not in progress."}, status=status.HTTP_400_BAD_REQUEST)

        if user not in [trade.initiator, trade.responder]:
            return Response({"error": "You are not a participant in this trade."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Receiver does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            trade=trade,
            sender=user,
            receiver=receiver,
            content=content
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        trade_id = request.query_params.get('trade_id')

        if not trade_id:
            return Response({"error": "Trade ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user not in [trade.initiator, trade.responder]:
            return Response({"error": "You are not a participant in this trade."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all messages related to the trade
        messages = Message.objects.filter(trade=trade).order_by('sent_at')

        # Filter messages based on the search query parameter
        search_query = request.query_params.get('search')
        if search_query is not None:
            messages = messages.filter(content__icontains=search_query)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(messages, request)

        # Serialize the messages
        serializer = MessageSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class DeleteMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        message_id = request.data.get('message_id')

        if not message_id:
            return Response({"error": "Message ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if message.sender != user:
            return Response({"error": "You are not the author of this message."}, status=status.HTTP_400_BAD_REQUEST)

        message.delete()
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_200_OK)
    
class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        trade_id = request.data.get('trade_id')
        rating = request.data.get('rating')
        feedback = request.data.get('feedback')

        if not trade_id or not rating:
            return Response({"error": "Trade ID and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if trade.status != 'Completed':
            return Response({"error": "Trade is not completed."}, status=status.HTTP_400_BAD_REQUEST)

        if user != trade.responder:
            return Response({"error": "You are not the responder of this trade."}, status=status.HTTP_400_BAD_REQUEST)

        if Review.objects.filter(trade=trade).exists():
            return Response({"error": "A review for this trade already exists."}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            trade=trade,
            reviewer=user,
            reviewee=trade.initiator,
            rating=rating,
            feedback=feedback
        )

        self.update_initiator_rating(trade.initiator)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_initiator_rating(self, initiator):
        average_rating = Review.objects.filter(reviewee=initiator).aggregate(Avg('rating'))['rating__avg']
        initiator.rating = average_rating if average_rating is not None else 0.00
        initiator.save()

class UpdateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        review_id = request.data.get('review_id')
        rating = request.data.get('rating')
        feedback = request.data.get('feedback')

        if not review_id or not rating:
            return Response({"error": "Review ID and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user != review.reviewer:
            return Response({"error": "You are not the author of this review."}, status=status.HTTP_400_BAD_REQUEST)

        review.rating = rating
        review.feedback = feedback
        review.save()

        self.update_initiator_rating(review.reviewee)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_initiator_rating(self, initiator):
        average_rating = Review.objects.filter(reviewee=initiator).aggregate(Avg('rating'))['rating__avg']
        initiator.rating = average_rating if average_rating is not None else 0.00
        initiator.save()

class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        review_id = request.data.get('review_id')

        if not review_id:
            return Response({"error": "Review ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user != review.reviewer:
            return Response({"error": "You are not the author of this review."}, status=status.HTTP_400_BAD_REQUEST)

        initiator = review.reviewee
        review.delete()

        self.update_initiator_rating(initiator)

        return Response({"message": "Review deleted successfully."}, status=status.HTTP_200_OK)

    def update_initiator_rating(self, initiator):
        average_rating = Review.objects.filter(reviewee=initiator).aggregate(Avg('rating'))['rating__avg']
        initiator.rating = average_rating if average_rating is not None else 0.00
        initiator.save()

class ListReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        trade_id = request.query_params.get('trade_id')

        if not trade_id:
            return Response({"error": "Trade ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Trade does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all reviews related to the trade
        reviews = Review.objects.filter(trade=trade)

        # Filter reviews based on the search query parameter
        search_query = request.query_params.get('search')
        if search_query is not None:
            reviews = reviews.filter(feedback__icontains=search_query)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(reviews, request)

        # Serialize the reviews
        serializer = ReviewSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class TradeListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        # Get all trades where the user is either the initiator or the responder
        trades = Trade.objects.filter(initiator=user) | Trade.objects.filter(responder=user)

        # Filter trades based on the search query parameter
        search_query = request.query_params.get('search')
        if search_query is not None:
            trades = trades.filter(title__icontains=search_query) | trades.filter(description__icontains=search_query)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(trades, request)

        # Serialize the trades
        serializer = TradeSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class TradeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            trade = Trade.objects.get(pk=pk)
        except Trade.DoesNotExist:
            return Response({"detail": "Trade not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is either the initiator or the responder
        if request.user != trade.initiator and request.user != trade.responder:
            return Response({"detail": "You do not have permission to view this trade."}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the trade
        serializer = TradeSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QueueListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trade_id, *args, **kwargs):
        try:
            trade = Trade.objects.get(pk=trade_id)
        except Trade.DoesNotExist:
            return Response({"detail": "Trade not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is the initiator of the trade
        if request.user != trade.initiator:
            return Response({"detail": "You do not have permission to view this queue."}, status=status.HTTP_403_FORBIDDEN)

        # Get all queues related to the trade
        queues = Queue.objects.filter(trade=trade)

        # Filter queues based on the search query parameter
        search_query = request.query_params.get('search')
        if search_query is not None:
            queues = queues.filter(user__username__icontains=search_query)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(queues, request)

        # Serialize the queues
        serializer = QueueSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filter users based on the search query parameter (skills offered)
        search_query = request.query_params.get('search')
        if search_query is not None:
            skills = Skill.objects.filter(name__icontains=search_query)
            users = CustomUser.objects.filter(skills_offered__in=skills).distinct().order_by('-rating')
        else:
            users = CustomUser.objects.all().order_by('-rating')

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(users, request)

        # Serialize the users
        serializer = UserSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
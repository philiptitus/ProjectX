from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
 
from rest_framework.decorators import permission_classes

from rest_framework import generics
from ..serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404


import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction



class deletePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        # Check if the user is either the author of the post or the owner of the post
        if request.user == post.user :
            post.delete()
            return Response("The Post Was Deleted Successfully")
        else:
            return Response("You are not allowed to delete this post", status=403)
        
  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class GetPostsView(APIView):
    def get(self, request):
        # Retrieve posts excluding posts from private accounts
        qs = Post.objects.all(
        )
        qs = Post.objects.exclude(caption__isnull=True).exclude(caption="").order_by('-created_date')



        name = request.query_params.get('name')
        if name is not None:
            qs = qs.filter(caption__icontains=name)

        # Use Django REST framework's built-in pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of posts per page
        result_page = paginator.paginate_queryset(qs, request)
        
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)




class GetPost(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)


 

from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from better_profanity import profanity
from itertools import chain
from django.shortcuts import get_object_or_404


class GetFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following = user.following.all()



        if not following:
            return Response({"detail": "You are not following anyone yet."})

        qs = Post.objects.filter(user__in=following.values('following'))
        vs = Post.objects.filter(user__in=following.values('following'), isSlice=True).order_by('-created_date')

        fs = Post.objects.filter(user=user, isSlice=False)


        qs = qs.exclude(albums__isnull=True).order_by('-created_date')
        fs = fs.exclude(albums__isnull=False)

        fs.delete()



        combined_qs = list(chain(qs, vs))

        combined_qs = sorted(combined_qs, key=lambda x: x.created_date, reverse=True)



        # Use Django REST framework's built-in pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of posts per page
        result_page = paginator.paginate_queryset(combined_qs, request)

        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


from rest_framework import generics


class GetAlbumView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        # Get the target user
        user = request.user


        # Your existing logic to retrieve and return data

        qs = Post.objects.filter(user=user).exclude(caption__isnull=True).exclude(caption="").order_by('-created_date')




        # Use Django REST framework's built-in pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of posts per page
        result_page = paginator.paginate_queryset(qs, request)

        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@permission_classes([IsAuthenticated])


class createPost(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        post = Post.objects.create(
            user=user,
            caption = '',
            description = '',
        )
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)



class updatePost(APIView):
    def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        data = request.data

        # Update fields if they are present in the request data
        if 'caption' in data:
            post.caption = data['caption']
        if 'description' in data:
            post.description = data['description']
        if 'isSlice' in data:
            post.isSlice = data['isSlice']
        if 'price' in data:
            post.price = data['price']
        if 'location' in data:
            post.location = data['location']

        # Save the updated post
        post.save()

        # Serialize the updated post
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)





@permission_classes([IsAuthenticated])
class Chat(APIView):

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        # Ensure that the receiver_id is provided and it corresponds to an existing user
        if not receiver_id or not CustomUser.objects.filter(id=receiver_id).exists():
            return Response({'detail': 'Invalid receiver_id'}, status=400)

        receiver = CustomUser.objects.get(id=receiver_id)

        # Check if the sender and receiver are the same user
        if sender == receiver:
            return Response({'detail': "Can't message yourself silly"}, status=400)

        # Create the message
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )



        return Response(MessageSerializer(message).data)


@permission_classes([IsAuthenticated])
class ChatList(APIView):

    def get(self, request):
        user = request.user

        # Retrieve all messages involving the user
        messages = Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('-timestamp')

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of posts per page
        result_page = paginator.paginate_queryset(messages, request)
        

        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



@permission_classes([IsAuthenticated])
class ChatDetail(APIView):

    def get(self, request, pk):
        user = request.user

        # Retrieve the specific message by its primary key (id)
        message = Message.objects.get(id=pk)

        # Check if the user is part of the message (either sender or receiver)
        if user == message.sender or user == message.receiver:
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Permission denied'}, status=403)
        



class AllMessagesWithUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Make sure the other user exists
        other_user = get_object_or_404(CustomUser, id=pk)

        # Retrieve all messages between the authenticated user and the other user
        messages = Message.objects.filter(
            (Q(sender=request.user, receiver=other_user) |
             Q(sender=other_user, receiver=request.user))
        ).order_by('-timestamp')

        # Update is_read only for messages where request.user is the receiver
        for message in messages.filter(receiver=request.user):
            message.is_read = True
            message.save()



        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of posts per page
        result_page = paginator.paginate_queryset(messages, request)
        

        # Serialize the messages
        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


from django.utils import timezone



class UsersEngagedInConversation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get a list of unique users with whom the authenticated user has exchanged messages
        # Both as sender and receiver
        users = CustomUser.objects.filter(
            Q(sent_messages__receiver=request.user) |
            Q(received_messages__sender=request.user)
        ).distinct()

        # Serialize the users
        serialized_users = UserSerializer(users, many=True, context={'request': request}).data

        # Add unread_count and last_message_timestamp fields to each user data
        for user_data in serialized_users:
            user = CustomUser.objects.get(pk=user_data['id'])

            # Check if the last message sent between the two users had request.user as a receiver
            last_message = Message.objects.filter(
                Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
            ).order_by('-timestamp').first()

            if last_message and last_message.receiver == request.user:
                user_data['unread_count'] = Message.get_unread_count(request.user, user)
                user_data['last_message_timestamp'] = last_message.timestamp
            else:
                user_data['unread_count'] = 0
                user_data['last_message_timestamp'] = None

        # Sort the list of users based on the last_message_timestamp in descending order
        serialized_users = sorted(
            serialized_users,
            key=lambda x: x['last_message_timestamp'] if x['last_message_timestamp'] is not None else timezone.now(),
            reverse=True
        )

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(serialized_users, request)

        return paginator.get_paginated_response(result_page)
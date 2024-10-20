from base.views.post_views import *
from base.views.user_views import *
from django.urls import path




urlpatterns = [

    path('posts/', GetPostsView.as_view(), name='get_posts'), 
    path('album/', GetAlbumView.as_view(), name='album'),
    path('new/', createPost.as_view(), name='new-post'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), ##
    path('register/', RegisterUser.as_view(), name='register'), ##
    path('profile/', GetUserProfile.as_view(), name='user-profile'),#
    path('delete/', deleteAccount.as_view(), name='delete'), ##
    path('chat/', Chat.as_view()),
    path('conversations/', UsersEngagedInConversation.as_view()),
    path('chats/<int:pk>/', AllMessagesWithUser.as_view()),
    path('update/<str:pk>/', updatePost.as_view(), name='post-update'), 
    path('<str:pk>/delete/', deletePost.as_view(), name='delete-post'),
    path('<str:pk>/', GetPost.as_view(), name='get_post'),









]

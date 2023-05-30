from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'insta'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('post/', login_required(views.PostCreate.as_view()), name='post_create'),
    path('post/chat/<int:pk>/', login_required(views.PostChat.as_view()), name='post_chat'),
    path('post/chat/reply/<int:pk>/', login_required(views.PostReply.as_view()), name='post_reply'),
    path('post/delete/<int:pk>/', login_required(views.PostDelete.as_view()), name='post_delete'),
    path('post/tag/<int:pk>', login_required(views.PostTags.as_view()), name='post_tag'),

    path('my/', login_required(views.MyPage.as_view()), name='my_page'),
    path('my/update/', login_required(views.MyPageUpdate.as_view()), name='my_page_update'),


    path('user/page/<int:pk>', views.UserPage.as_view(), name='user_page'),

    path('search/', login_required(views.SearchList.as_view()), name='search'),

    path('dm/', login_required(views.FollowUserList.as_view()), name='follow_user'),
    path('dm/<int:pk>/', login_required(views.DMChatList.as_view()), name='dm'),

    path('like/<int:pk>/', login_required(views.Like.as_view()), name='like'),
    path('bookmark/', login_required(views.BookMark.as_view()), name='bookmark'),

    # path('')
]
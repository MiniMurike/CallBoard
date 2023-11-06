from django.urls import path, include

from Posts.views import (
    PostList, CreatePost, PostDetail, PostUpdate, PostDelete, CreateReply, DetailReply
)
from accounts.views import Profile

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('edit/<int:pk>', PostUpdate.as_view(), name='post_edit'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('reply/', CreateReply.as_view(), name='create_reply'),
    path('reply/<int:pk>', DetailReply.as_view(), name='detail_reply'),
    path('profile/<int:pk>', Profile.as_view(), name='profile'),
]

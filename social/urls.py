from django.urls import path
from social.views import PostDetailView, PostListView, PostEditView


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post_edit')
]
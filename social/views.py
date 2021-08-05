from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

class PostListView(LoginRequiredMixin ,View):

    def get(self, request, *args, **kwags):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list' : posts,
            'form' : form
        } 

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list' : posts,
            'form' : form
        } 

        return render(request, 'social/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwrfags):
        post = Post.objects.get(pk =pk)
        form = CommentForm()

        comment = Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            "post" : post,
            'form' : form,
            'comment' : comment
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwrfags):
        post = Post.objects.get(pk =pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comment = Comment.objects.filter(post = post).order_by('-created_on')

        context = {
            "post" : post,
            'form' : form,
            'comment' : comment
        }

        return render(request, 'social/post_detail.html', context)

class PostEditView(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs = {'pk' : pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs = {'pk' : pk})   

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 


class ProfileView(View):
    def get(self, request, pk, *args, **kwags):
        profile = UserProfile.objects.get(pk = pk)
        user = profile.user
        post = Post.objects.filter(author = user).order_by('created_on')

        context = {
            'user': user,
            'profile' : profile,
            'post' : post
        }

        return render(request, 'social/profile.html', context)

class ProfileEditView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = UserProfile
    fields = ['name', 'bio', 'birthday', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse_lazy('profile', kwargs = {'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user 
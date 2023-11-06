from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from Posts.filters import PostFilter
from Posts.forms import CreatePostForm, ReplyCreateForm
from Posts.models import Post, Replies
from main.tasks import send_single_email


class PostList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, qs)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        try:
            if self.request.session['alert']:
                context['alert'] = self.request.session['alert']
                self.request.session['alert'] = None
        except Exception as e: pass

        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        request.session['post_id'] = request.POST.get('post_id')
        return redirect('create_reply')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    context_object_name = 'post'
    form_class = CreatePostForm
    template_name = 'create_post.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete.html'
    success_url = '/'


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.creator = self.request.user

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = CreatePostForm
        context = {
            'form': form
        }

        return render(request, 'create_post.html', context)


class CreateReply(LoginRequiredMixin, CreateView):
    model = Replies
    form_class = ReplyCreateForm
    template_name = 'create_reply.html'

    def form_valid(self, form):
        reply = form.save(commit=False)

        reply.user = self.request.user
        reply.post = Post.objects.get(id=int(self.request.POST.get('post')))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateReply, self).get_context_data(**kwargs)

        if self.request.session['post_id'] is not None:
            context['post'] = Post.objects.get(id=self.request.session['post_id'])
            self.request.session['post_id'] = None

        return context


class DetailReply(LoginRequiredMixin, DetailView):
    model = Replies
    context_object_name = 'reply'
    template_name = 'reply_detail.html'

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        post_id = request.POST.get('post')
        post = Post.objects.get(id=post_id)

        replier_id = request.POST.get('replier')
        replier = User.objects.get(id=replier_id)

        author_id = request.POST.get('author')
        author = User.objects.get(id=author_id)

        if action == 'confirm':
            subject = _('Reply confirmation')
            text_content = '\n'.join([
                _(f'Your reply to [{post.role}] {post.title} has been confirmed.'),
                _(f'In order to continue: private message to post author: {User.objects.get(id=author.id).email}')
            ])
            send_single_email.delay(
                subject=subject,
                text=text_content,
                email=replier.email,
            )
        elif action == 'deny':
            subject = _('Your reply denied')
            text_content = '\n'.join([
                _(f'Your reply to [{post.role}] {post.title} has been denied'),
            ])
            send_single_email.delay(
                subject=subject,
                text=text_content,
                email=replier.email,
            )

            Replies.objects.filter(
                post__id=post_id,
                user__id=replier_id,
            ).delete()

        request.session['alert'] = _('Notification has been send to replier')
        return redirect('post_list')

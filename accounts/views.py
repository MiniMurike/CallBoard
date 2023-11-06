from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.utils.translation import gettext as _

from Posts.models import Replies
from accounts.forms import SignupForm
from main.tasks import send_emails_to_users


class Signup(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class Profile(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'model_user'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)

        user_id = self.request.user.id
        context['replied_from_user'] = Replies.objects.filter(user=user_id)
        context['replies_to_user'] = Replies.objects.filter(post__creator=user_id)

        return context


def send_emails(request):
    if request.method == 'GET':
        return render(request, 'send_emails.html')
    elif request.method == 'POST':
        text = request.POST.get('text')
        emails = list(User.objects.all().values_list('email', flat=True))

        send_emails_to_users.delay(
            subject=_('Info from the CallBoard'),
            text=text,
            emails=emails,
        )

        return redirect('post_list')


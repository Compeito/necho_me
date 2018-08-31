from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import os
import random

from account.models import User
from .models import Nyaaan
from .utils import get_user_api, gen_unique_slug, AltPaginationListView
from .forms import NyaaanForm


def top(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'core/top.html')


@login_required
def home(request):
    form = NyaaanForm()
    if request.method == 'POST':
        form = NyaaanForm(request.POST, request.FILES)
        if form.is_valid():
            api = get_user_api(request.user)

            nyaaan_slug = gen_unique_slug(5, Nyaaan)
            echo = 'にゃーん'
            if random.randint(1, 30) == 1:
                echo = random.choice(settings.ECHO_LIST)

            if not settings.DEBUG:
                tweet = api.PostUpdate(f'{echo} https://necho.me/{nyaaan_slug}')
                tweet_dict = tweet.AsDict()
            else:
                print(f'{echo} https://necho.me/{nyaaan_slug}')
                tweet_dict = {}

            Nyaaan.objects.create(
                user=request.user,
                text=request.POST['text'],
                tweet=tweet_dict,
                echo=echo,
                slug=nyaaan_slug
            )

            messages.success(request, 'にゃーんされました')
            return redirect(f'/{nyaaan_slug}')

    return render(request, 'core/form.html', {'form': form})


def detail(request, slug):
    _nyaaan = get_object_or_404(Nyaaan, slug=slug)
    return render(request, 'core/detail.html', {'nyaaan': _nyaaan})


def delete(request, slug):
    _nyaaan = get_object_or_404(Nyaaan, slug=slug)
    if request.user == _nyaaan.user:
        if not settings.DEBUG:
            _nyaaan.delete()
        return JsonResponse({'code': 100})
    else:
        return JsonResponse({'code': 101})


def users(request, username):
    account = get_object_or_404(User, username=username)
    return render(request, 'core/users.html', {'account': account})


class UserPage(AltPaginationListView):
    template_name = 'core/users.html'
    context_object_name = 'nyaaans'
    paginate_by = 5

    def get_queryset(self):
        nyaaans = Nyaaan.objects.filter(user__username=self.kwargs['username'])
        return nyaaans.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = get_object_or_404(User, username=self.kwargs['username'])
        return context


def favicon(request):
    with open(os.path.join(settings.BASE_DIR, 'static', 'favicon.ico')) as f:
        response = HttpResponse(f.buffer, content_type="image/x-icon")
        response["Content-Disposition"] = "filename=favicon.ico"
        return response

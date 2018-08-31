from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from core.utils import get_user_api
from .forms import UserSettingsForm


@login_required
def login_after_redirect(request):
    user = request.user
    if not user.data_imported:
        try:
            api = get_user_api(request.user)
            user.json = api.VerifyCredentials().AsDict()
            user.save()
        except:
            return redirect('/')

    return redirect('/')


@login_required
@staff_member_required
def user_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=user)

        if not user.username == request.POST['username']:
            form.add_error('username', 'ユーザー名は変更できません')
            return render(request, 'account/settings.html', {'form': form})

        if form.is_valid():
            form.save()
            return render(request, 'account/settings.html', {'form': form, 'change_success': True})

    form = UserSettingsForm(instance=user)
    return render(request, 'account/settings.html', {'form': form})

from django import forms

from .models import User


class UserSettingsForm(forms.ModelForm):
    profile_icon = forms.ImageField(label='アイコン画像', required=False)
    username = forms.CharField(label='ユーザー名',
                               widget=forms.TextInput(attrs={'readonly': True}))
    first_name = forms.CharField(label='表示名')
    description = forms.CharField(
        widget=forms.Textarea,
        label='説明文',
        max_length=300,
        help_text='300字まで',
        required=False
    )

    class Meta:
        model = User
        fields = ('profile_icon', 'username', 'first_name', 'description')

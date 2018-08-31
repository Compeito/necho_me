from django import forms


class NyaaanForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'なんかかいとけ', 'rows': 4}),
        label='',
        max_length=500,
        help_text='500文字まで'
    )

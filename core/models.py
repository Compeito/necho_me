from django.db import models
from django.utils import timezone

import jsonfield


class Nyaaan(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='echoes')
    tweet = jsonfield.JSONField()
    text = models.TextField(max_length=500)
    echo = models.CharField(max_length=255, default='にゃーん')
    slug = models.SlugField()
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def short_text(self):
        if len(self.text) > 50:
            return self.text[:50] + '…'
        else:
            return self.text

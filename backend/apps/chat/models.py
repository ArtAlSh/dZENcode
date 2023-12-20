from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="messages", null=True)
    homepage = models.URLField(null=True, blank=True)
    message = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}: {self.message[:15]}'

    class Meta:
        db_table = "messages"
        ordering = ["-date"]

    @property
    def count_comments(self):
        return self.messages.count()

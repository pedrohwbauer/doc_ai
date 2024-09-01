from django.db import models

class Message(models.Model):
    SYSTEM = 0
    ASSISTANT = 10
    USER = 20
    ROLE_CHOICES = (
        (SYSTEM, "System"),
        (ASSISTANT, "Assistant"),
        (USER, "User"),
    )

    role = models.IntegerField(choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    
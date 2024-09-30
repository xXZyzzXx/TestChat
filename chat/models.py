from django.contrib.auth.models import User
from django.db import models

from utils.models import TimeStampModel, UUIDModel


class Thread(UUIDModel, TimeStampModel):
    participants = models.ManyToManyField(User, related_name="threads")

    @property
    def participants_names(self) -> str:
        return ", ".join([user.username for user in self.participants.all()])

    def __str__(self):
        return f"Thread between {self.participants_names}"


class Message(UUIDModel, TimeStampModel):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField()
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in thread {self.thread.id}"

from typing import Set

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from chat.models import Message, Thread


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ThreadCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Thread
        fields = ["id", "participant_ids", "created_at", "updated_at"]

    def validate_participant_ids(self, value) -> Set[int]:
        """Validate that participants do not exceed the limit"""
        user_id: int = self.context["request"].user.id

        participants: Set[int] = set(value)
        participants.add(user_id)

        participants_count: int = len(participants)
        if participants_count != settings.MAX_PARTICIPANTS_PER_THREAD:
            raise serializers.ValidationError(
                f"The thread must have {settings.MAX_PARTICIPANTS_PER_THREAD} participants."
            )
        if not User.objects.filter(id__in=participants).count() == participants_count:
            raise serializers.ValidationError("One or more users do not exist.")

        return participants

    @transaction.atomic
    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        thread = Thread.objects.create()
        thread.participants.set(participant_ids)
        return thread

    @transaction.atomic
    def update(self, instance, validated_data):
        if participant_ids := validated_data.get("participant_ids"):
            participant_ids = self.validate_participant_ids(participant_ids)
            instance.participants.set(participant_ids)
        return instance


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = "__all__"


class UnreadMessagesCountSerializer(serializers.Serializer):
    unread_messages = serializers.IntegerField()

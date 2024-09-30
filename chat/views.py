from typing import Set

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.models import Message, Thread
from chat.serializers import (
    MessageSerializer,
    ThreadCreateSerializer,
    ThreadSerializer,
    UnreadMessagesCountSerializer,
)
from chat.services import ThreadService


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Thread]:
        user: User = self.request.user
        return Thread.objects.filter(participants=user)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a new thread or return the existing one"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant_ids: Set[int] = serializer.validated_data["participant_ids"]

        thread, created = ThreadService.get_or_create_thread(
            participants=participant_ids,
        )
        output_serializer = ThreadSerializer(
            thread,
        )
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["GET"], url_path="messages")
    def get_messages(self, request: Request, *args, **kwargs) -> Response:
        """Returns related messages for the thread"""
        thread: Thread = self.get_object()
        messages: QuerySet[Message] = thread.messages.all()
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ThreadCreateSerializer
        else:
            return ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: MessageSerializer) -> None:
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=["PATCH"], url_path="mark-as-read")
    def mark_as_read(self, request: Request, *args, **kwargs) -> Response:
        message: Message = self.get_object()
        message.is_read = True
        message.save(update_fields=["is_read"])
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], url_path="unread-count")
    def unread_messages_count(self, request: Request) -> Response:
        user: User = request.user
        count: int = Message.objects.filter(
            thread__participants=user, is_read=False
        ).count()
        serializer = UnreadMessagesCountSerializer({"unread_messages": count})
        return Response(serializer.data)

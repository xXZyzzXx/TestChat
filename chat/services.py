from typing import Set, Tuple

from django.conf import settings
from django.db.models import Count, QuerySet

from chat.exceptions import InvalidParticipantsCount
from chat.models import Thread


class ThreadService:
    """Repository for Thread model"""

    @classmethod
    def get_or_create_thread(cls, participants: Set[int]) -> Tuple[Thread, bool]:
        """Get or create a thread with participants"""
        if len(participants) != settings.MAX_PARTICIPANTS_PER_THREAD:
            raise InvalidParticipantsCount()

        existing_threads: QuerySet[Thread] = (
            Thread.objects.annotate(
                num_participants=Count("participants", distinct=True)
            )
            .filter(participants__id__in=participants)
            .distinct()
        )
        for thread in existing_threads:
            thread_participants: Set[int] = set(
                thread.participants.values_list("id", flat=True)
            )
            if thread_participants == participants:
                return thread, False

        thread: Thread = Thread.objects.create()
        thread.participants.set(participants)
        return thread, True

from django.conf import settings
from rest_framework.exceptions import APIException


class InvalidParticipantsCount(APIException):
    detail = (
        f"The thread must have {settings.MAX_PARTICIPANTS_PER_THREAD} participants."
    )

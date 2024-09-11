import os
import logging
from logging.handlers import RotatingFileHandler


class UserFilter(logging.Filter):
    def filter(self, record):
        request = getattr(record, "request", None)
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                record.user = f"{user.username} ({user.id})"
            else:
                record.user = "AnonymousUser"
        else:
            record.user = "Anonymous"
        return True

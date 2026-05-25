"""
app/models/__init__.py

Импортируем все модели здесь, чтобы Alembic видел их при автогенерации миграций.
"""
from .base import Base, TimestampMixin, UUIDMixin
from .users import User, UserRole
from .subscriptions import TariffPlan, TariffSlug, Subscription, SubscriptionStatus
from .devices import Device, DeviceType
from .tickets import Ticket, TicketStatus, TicketPriority, TicketDevice
from .messages import Message, MessageType
from .reviews import Review
from .otp import OTPCode

__all__ = [
    "Base",
    "TimestampMixin",
    "UUIDMixin",
    # Users
    "User",
    "UserRole",
    # Subscriptions
    "TariffPlan",
    "TariffSlug",
    "Subscription",
    "SubscriptionStatus",
    # Devices
    "Device",
    "DeviceType",
    # Tickets
    "Ticket",
    "TicketStatus",
    "TicketPriority",
    "TicketDevice",
    # Messages
    "Message",
    "MessageType",
    # Reviews
    "Review",
    # OTP
    "OTPCode",
]
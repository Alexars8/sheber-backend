"""
messages.py — сообщения чата внутри тикета.

Чат привязан к конкретной заявке (ticket).
Поддерживает текстовые сообщения и файлы-вложения.
"""
import enum
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .tickets import Ticket
    from .users import User


class MessageType(str, enum.Enum):
    text       = "text"
    image      = "image"
    file       = "file"
    system     = "system"   # Системное сообщение: «Мастер принял заявку»


class Message(UUIDMixin, TimestampMixin, Base):
    """
    Одно сообщение в чате тикета.
    """
    __tablename__ = "messages"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="NULL для системных сообщений"
    )

    message_type: Mapped[MessageType] = mapped_column(
        Enum(MessageType), default=MessageType.text, nullable=False
    )

    # Для текстовых сообщений
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Для файлов / изображений
    file_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Прочитано ли получателем
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Связи ──────────────────────────────────────────────────────────
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="messages")
    sender: Mapped[Optional["User"]] = relationship("User", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} ticket_id={self.ticket_id} type={self.message_type}>"
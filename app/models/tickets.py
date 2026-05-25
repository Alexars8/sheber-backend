"""
tickets.py — заявки (тикеты) на IT-обслуживание.

Жизненный цикл статуса:
  new → assigned → in_progress → done
                 ↘ cancelled

TicketDevice — связь M2M между заявкой и затронутыми устройствами.
"""
import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Text, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .users import User
    from .devices import Device
    from .messages import Message
    from .reviews import Review


class TicketStatus(str, enum.Enum):
    new         = "new"          # Создана, мастер ещё не назначен
    assigned    = "assigned"     # Мастер назначен, ждём даты
    in_progress = "in_progress"  # Мастер начал работу
    done        = "done"         # Успешно закрыта
    cancelled   = "cancelled"    # Отменена клиентом или системой


class TicketPriority(str, enum.Enum):
    normal = "normal"
    urgent = "urgent"   # Срочный вызов — доп. оплата


class Ticket(UUIDMixin, TimestampMixin, Base):
    """
    Основная сущность — заявка на выезд мастера.
    """
    __tablename__ = "tickets"

    # ── Участники ──────────────────────────────────────────────────────
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    master_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=True
    )

    # ── Контент ────────────────────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.new, nullable=False
    )
    priority: Mapped[TicketPriority] = mapped_column(
        Enum(TicketPriority), default=TicketPriority.normal, nullable=False
    )

    # Внеплановый ли выезд, превышающий лимит тарифа?
    is_extra_visit: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Если выезд платный, фиксируем стоимость
    extra_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)

    # Таймлайн
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Связи ──────────────────────────────────────────────────────────
    client: Mapped["User"] = relationship(
        "User", foreign_keys=[client_id], back_populates="client_tickets"
    )
    master: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[master_id], back_populates="master_tickets"
    )
    ticket_devices: Mapped[List["TicketDevice"]] = relationship(
        "TicketDevice", back_populates="ticket", cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="ticket", cascade="all, delete-orphan"
    )
    review: Mapped[Optional["Review"]] = relationship(
        "Review", back_populates="ticket", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Ticket id={self.id} status={self.status} priority={self.priority}>"


class TicketDevice(Base):
    """
    M2M: какие устройства фигурируют в заявке.
    Дополнительное поле — примечание к конкретному устройству в контексте заявки.
    """
    __tablename__ = "ticket_devices"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"),
        primary_key=True
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"),
        primary_key=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Связи ──────────────────────────────────────────────────────────
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="ticket_devices")
    device: Mapped["Device"] = relationship("Device", back_populates="ticket_links")
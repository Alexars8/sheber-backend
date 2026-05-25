"""
users.py — модель пользователей (клиентов и мастеров).

Роли:
  client  — бизнес-клиент, создаёт заявки, имеет тариф.
  master  — IT-мастер, выполняет заявки, имеет рейтинг.
"""
import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .devices import Device
    from .subscriptions import Subscription
    from .tickets import Ticket
    from .messages import Message
    from .reviews import Review


class UserRole(str, enum.Enum):
    client = "client"
    master = "master"


class User(UUIDMixin, TimestampMixin, Base):
    """
    Единая таблица пользователей.
    Разделение на клиента/мастера — через поле `role`.
    """
    __tablename__ = "users"

    # ── Общие поля ─────────────────────────────────────────────────────
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Поля только для клиентов ────────────────────────────────────────
    # Юридические данные / Название ТОО / ИП
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bin_iin: Mapped[Optional[str]] = mapped_column(String(12), nullable=True, comment="БИН или ИИН для документов")
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, comment="Адрес офиса компании")

    # ── Поля только для мастеров ────────────────────────────────────────
    rating: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    # Навыки / специализация
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Ссылка на аватар (хранится в S3/локально, в БД — путь)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    # ── Связи (клиент) ─────────────────────────────────────────────────
    devices: Mapped[List["Device"]] = relationship(
        "Device", back_populates="owner", cascade="all, delete-orphan"
    )
    subscriptions: Mapped[List["Subscription"]] = relationship(
        "Subscription", back_populates="client", cascade="all, delete-orphan"
    )
    client_tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket", foreign_keys="Ticket.client_id", back_populates="client"
    )

    # ── Связи (мастер) ─────────────────────────────────────────────────
    master_tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket", foreign_keys="Ticket.master_id", back_populates="master"
    )
    reviews_received: Mapped[List["Review"]] = relationship(
        "Review", foreign_keys="Review.master_id", back_populates="master"
    )
    reviews_given: Mapped[List["Review"]] = relationship(
        "Review", foreign_keys="Review.client_id", back_populates="client"
    )

    # ── Сообщения (общие) ──────────────────────────────────────────────
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="sender", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone} role={self.role}>"
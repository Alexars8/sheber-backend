"""
subscriptions.py — тарифы и подписки.

TariffPlan — справочник тарифов (Базовый / Бизнес / Премиум).
Subscription — активная подписка конкретного клиента.
"""
import enum
import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, Date, Enum, ForeignKey,
    Integer, Numeric, String, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .users import User


class TariffSlug(str, enum.Enum):
    base     = "base"
    business = "business"
    premium  = "premium"


class SubscriptionStatus(str, enum.Enum):
    active    = "active"
    paused    = "paused"   # клиент поставил на паузу
    cancelled = "cancelled"
    expired   = "expired"


class TariffPlan(UUIDMixin, TimestampMixin, Base):
    """
    Справочник тарифов. Изменяется редко — только администратором.
    Цены в тенге (KZT), хранятся как Numeric для точности.
    """
    __tablename__ = "tariff_plans"

    slug: Mapped[TariffSlug] = mapped_column(
        Enum(TariffSlug), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price_monthly: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Лимиты тарифа
    max_devices: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    included_visits: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        comment="Кол-во бесплатных выездов в месяц"
    )
    
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<TariffPlan slug={self.slug} price={self.price_monthly}>"


class Subscription(UUIDMixin, TimestampMixin, Base):
    """
    Текущая активная подписка клиента.
    История хранится через старые записи (cancelled/expired).
    """
    __tablename__ = "subscriptions"

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tariff_plans.id"), nullable=False
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus), default=SubscriptionStatus.active, nullable=False
    )

    # Период подписки
    started_at: Mapped[date] = mapped_column(Date, nullable=False)
    next_billing_at: Mapped[date] = mapped_column(Date, nullable=False)
    cancelled_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Использование за текущий период (сбрасывается при продлении)
    visits_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Платёжные реквизиты (токенизированные, не raw-данные карты)
    payment_method: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True,
        comment="Например: 'kaspi:••••4521'"
    )

    # ── Связи ──────────────────────────────────────────────────────────
    client: Mapped["User"] = relationship("User", back_populates="subscriptions")
    plan: Mapped["TariffPlan"] = relationship("TariffPlan")

    def __repr__(self) -> str:
        return f"<Subscription client_id={self.client_id} status={self.status}>"
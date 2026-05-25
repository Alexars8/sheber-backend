"""
devices.py — устройства клиентов, которые обслуживаются по подписке.
"""
import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .users import User
    from .tickets import TicketDevice


class DeviceType(str, enum.Enum):
    computer = "computer"   # ПК / ноутбук
    printer  = "printer"    # Принтер / МФУ
    router   = "router"     # Роутер / сетевое оборудование
    laptop   = "laptop"     # Ноутбук (отдельно от десктопа)
    server   = "server"     # Сервер
    other    = "other"      # Прочее


class Device(UUIDMixin, TimestampMixin, Base):
    """
    Единица техники, закреплённая за клиентом.
    Кол-во устройств ограничено тарифом (max_devices).
    """
    __tablename__ = "devices"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    device_type: Mapped[DeviceType] = mapped_column(
        Enum(DeviceType), nullable=False, default=DeviceType.other
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Модель устройства, напр. 'Dell OptiPlex 7090'"
    )
    os_firmware: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True,
        comment="ОС или прошивка, напр. 'Windows 11', 'RouterOS'"
    )
    serial_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Связи ──────────────────────────────────────────────────────────
    owner: Mapped["User"] = relationship("User", back_populates="devices")
    ticket_links: Mapped[List["TicketDevice"]] = relationship(
        "TicketDevice", back_populates="device", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Device id={self.id} name={self.name} owner_id={self.owner_id}>"
"""
otp.py — OTP-коды для авторизации по номеру телефона.
"""
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin, UUIDMixin

class OTPCode(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "otp_codes"

    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    code_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<OTPCode phone={self.phone} used={self.is_used}>"
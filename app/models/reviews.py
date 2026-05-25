    """
reviews.py — отзывы клиентов о мастере после закрытия заявки.
"""
import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .users import User
    from .tickets import Ticket

class Review(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="review_rating_range"),
    )

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"),
        unique=True, nullable=False
    )
    master_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Связи
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="review")
    master: Mapped["User"] = relationship(
        "User", foreign_keys=[master_id], back_populates="reviews_received"
    )
    client: Mapped["User"] = relationship(
        "User", foreign_keys=[client_id], back_populates="reviews_left"
    )
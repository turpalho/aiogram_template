from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .users import User
    from .posts import Post


class File(Base, TimestampMixin):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(BigInteger,
                                    primary_key=True)
    image_id: Mapped[str] = mapped_column(index=True)
    post_id: Mapped[int] = mapped_column(BigInteger,
                                         ForeignKey("posts.id", ondelete='CASCADE'))

    post: Mapped["Post"] = relationship(back_populates="files")

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self) -> str:
        return f"Image: #{self.id}"

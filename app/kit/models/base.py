from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel
from sqlmodel import TIMESTAMP, Field, MetaData, SQLModel

from app.kit.utils import generate_uuid, utc_now

_metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_N_label)s",
        "uq": "%(table_name)s_%(column_0_N_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_N_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)


class RecordMixin(BaseModel):
    id: UUID4 = Field(
        default_factory=generate_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )
    # TODO: type ignore due to incompatibility for timestamp, sqlmodel, and mypy
    created_at: datetime = Field(  # type: ignore
        sa_type=TIMESTAMP(timezone=True),
        default_factory=utc_now,
        nullable=False,
    )
    updated_at: datetime = Field(  # type: ignore
        sa_type=TIMESTAMP(timezone=True),
        default_factory=utc_now,
        nullable=False,
        sa_column_kwargs={"onupdate": utc_now},
    )
    deleted_at: Optional[datetime] = Field(  # type: ignore
        sa_type=TIMESTAMP(timezone=True),
        nullable=True,
    )


class Model(SQLModel):
    __abstract__ = True
    metadata = _metadata


class RecordModel(Model, RecordMixin):
    __abstract__ = True

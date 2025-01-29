from sqlmodel import Field

from app.kit.models import RecordModel


class Items(RecordModel, table=True):
    __tablename__ = "items"

    name: str = Field(nullable=False, unique=True)
    count: int = Field(1, nullable=False, gt=-1)
    description: str = Field(nullable=True)

from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class ItemsBase(BaseModel):
    name: str
    count: int = 1
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "casa dragones tequila",
            }
        }


class ItemsCreate(ItemsBase): ...


class ItemsUpdate(ItemsBase): ...


class ItemsDB(BaseModel):
    id: UUID4
    name: str
    count: int
    description: str | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

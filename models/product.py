from pydantic import BaseModel, Field, validator
from typing import List

class SizeEntry(BaseModel):
    size: str
    quantity: int = Field(..., ge=0, description="Quantity must be 0 or greater")

class ProductCreate(BaseModel):
    name: str = Field(..., max_length=20, description="Name max 20 characters")
    price: float = Field(..., ge=0, description="Price must be >= 0")
    size: List[SizeEntry]

    @validator("name")
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty or only spaces")
        return value

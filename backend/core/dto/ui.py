from pydantic import BaseModel
from typing import Optional
from .enums import SeverityLevel


class CTA(BaseModel):
    label: str
    type: str  # primary | secondary | ghost


class UIDecoration(BaseModel):
    badge: Optional[str] = None
    severity: SeverityLevel
    icon: str
    cta: Optional[CTA] = None

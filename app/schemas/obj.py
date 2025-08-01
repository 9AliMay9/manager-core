from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ObjCreate(BaseModel):
    dtgs: str  # Unique identifier
    ctgr_b: str  # Foreign key binding category
    dst: Optional[str] = None  # Optional description
    ctgr: Optional[str] = None  # Optional category


class ObjUpdate(BaseModel):
    dst: Optional[str] = None
    ctgr: Optional[str] = None
    ctgr_b: Optional[str] = None  # Optional update to binding category


class ObjListOut(BaseModel):
    dtgs: str  # Only identifier for listing
    
    class Config:
        from_attributes = True


class SbjRefOut(BaseModel):
    dtgs: str  # Linked Sbj identifier

    class Config:
        from_attributes = True


class ObjDetailOut(BaseModel):
    dtgs: str
    dst: Optional[str] = None
    ctgr: Optional[str] = None
    ctgr_b: str
    etpr: datetime
    ltpr: datetime
    sbj: Optional[SbjRefOut] = None  # Linked Sbj, if any

    class Config:
        from_attributes = True

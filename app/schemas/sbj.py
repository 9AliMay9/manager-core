from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SbjCreate(BaseModel):
    dtgs: str  # Unique identifier
    ctgr_b: str  # Foreign key binding category
    dst: Optional[str] = None  # Optional description
    ctgr: Optional[str] = None  # Optional category


class SbjUpdate(BaseModel):
    dst: Optional[str] = None  # Optional update for description
    ctgr: Optional[str] = None  # Optional update for category


class ObjBrief(BaseModel):
    dtgs: str  # Object identifier

    class Config:
        from_attributes = True


class SbjListOut(BaseModel):
    dtgs: str
    ctgr_b: str
    objs: List[ObjBrief] = []  # Related Obj list (brief form)

    class Config:
        from_attributes = True


class ObjRefOut(BaseModel):
    dtgs: str
    ctgr: Optional[str] = None  # Optional category of linked Obj

    class Config:
        from_attributes = True


class SbjDetailOut(BaseModel):
    dtgs: str
    ctgr_b: str
    dst: Optional[str] = None
    ctgr: Optional[str] = None
    etpr: datetime  # Entry timestamp
    ltpr: datetime  # Last updated timestamp
    objs: List[ObjRefOut] = []  # Related Obj list with category

    class Config:
        from_attributes = True


class SbjBriefOut(BaseModel):
    dtgs: str  # Only identifier shown

    class Config:
        from_attributes = True

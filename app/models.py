from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


# Base class for declarative models
class Base(DeclarativeBase):
    pass


# Subject Entity
class Sbj(Base):
    __tablename__ = "sbjs"

    dtgs = Column(String, primary_key=True, index=True)  # Unique tag
    dst = Column(String, nullable=True)  # Optionall description
    ctgr = Column(String, nullable=True)  # Optional category
    ctgr_b = Column(String, unique=True, nullable=False)  # Binding catagory (used as FK)

    etpr = Column(DateTime, default=datetime.utcnow, nullable=False)  # Entity creation time
    ltpr = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Last updated time

    # One-to-many relationship to Obj (by ctgr_b)
    objs = relationship(
            "Obj",
            back_populates="sbj",
            primaryjoin="Sbj.ctgr_b==foreign(Obj.ctgr_b)",
    )


# Object Entity
class Obj(Base):
    __tablename__ = "objs"

    dtgs = Column(String, primary_key=True, index=True)  # Unique tag
    dst = Column(String, nullable=True)  # Optional description
    ctgr = Column(String, nullable=True)  # Optional category
    ctgr_b = Column(String, ForeignKey("sbjs.ctgr_b"), nullable=False)  # FK to sbj.ctgr_b
    
    etpr = Column(DateTime, default=datetime.utcnow, nullable=False)  # Entitu creation time
    ltpr = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Last updated time

    # Reference back to owing Sbj
    sbj = relationship(
            "Sbj",
            back_populates="objs",
            primaryjoin="foreign(Obj.ctgr_b)==Sbj.ctgr_b",
    )

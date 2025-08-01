from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from fastapi import HTTPException, status

from app import models, schemas


def create_obj(db: Session, obj_in: schemas.ObjCreate) -> schemas.ObjDetailOut:
    """Create a new Obj, ensure dtgs uniqueness and valid sbj reference"""
    try:    
        if db.query(models.Obj).filter(models.Obj.dtgs == obj_in.dtgs).first():
            raise HTTPException(status_code=400, detail="Obj with dtgs already exists")

        if not db.query(models.Sbj).filter(models.Sbj.ctgr_b == obj_in.ctgr_b).first():
            raise HTTPException(status_code=400, detail="Associated Sbj with given ctgr_b not found")
        
        obj = models.Obj(**obj_in.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)

        sbj = db.query(models.Sbj).filter(models.Sbj.ctgr_b == obj.ctgr_b).first()
        sbj_data = {"dtgs": sbj.dtgs, "ctgr": sbj.ctgr} if sbj else None

        return schemas.ObjDetailOut.model_validate({**obj.__dict__, "sbj": sbj_data})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def read_all_objs(db: Session) -> list[schemas.ObjListOut]:
    """Return all Obj entries"""
    try:
        objs = db.query(models.Obj).all()
        return [schemas.ObjListOut.model_validate(obj) for obj in objs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def read_obj_by_dtgs(db: Session, dtgs: str) -> schemas.ObjDetailOut:
    """Return a specific Obj by dtgs, including linked Sbj info"""
    try:
        obj = db.query(models.Obj).filter(models.Obj.dtgs == dtgs).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Obj not found")

        sbj = db.query(models.Sbj).filter(models.Sbj.ctgr_b == obj.ctgr_b).first()
        sbj_data = {"dtgs": sbj.dtgs, "ctgr": sbj.ctgr} if sbj else None

        return schemas.ObjDetailOut.model_validate({**obj.__dict__, "sbj": sbj_data})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def read_objs_by_ctgr(db: Session, ctgr: str) -> list[schemas.ObjListOut]:
    """Return Obj entries filtered by category"""
    try:
        objs = db.query(models.Obj).filter(models.Obj.ctgr == ctgr).all()
        return [schemas.ObjListOut.model_validate(obj) for obj in objs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def update_obj(db: Session, dtgs: str, obj_in: schemas.ObjUpdate) -> schemas.ObjDetailOut:
    """Update an existing Obj entry"""
    try:
        obj = db.query(models.Obj).filter(models.Obj.dtgs == dtgs).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Obj not found")

        if (
            obj.dst == obj_in.dst and
            obj.ctgr == obj_in.ctgr and
            obj.ctgr_b == obj_in.ctgr_b
        ):
            raise HTTPException(status_code=400, detail="No change detected")
    
        obj.dst = obj_in.dst
        obj.ctgr = obj_in.ctgr
        obj.ctgr_b = obj_in.ctgr_b
        db.commit()
        db.refresh(obj)

        sbj = db.query(models.Sbj).filter(models.Sbj.ctgr_b == obj.ctgr_b).first()
        sbj_data = {"dtgs": sbj.dtgs, "ctgr": sbj.ctgr} if sbj else None
        
        return schemas.ObjDetailOut.model_validate({**obj.__dict__, "sbj": sbj_data})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def delete_obj(db: Session, dtgs: str) -> dict:
    """Delete an Obj by dtgs"""
    try:
        obj = db.query(models.Obj).filter(models.Obj.dtgs == dtgs).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Obj not found")

        db.delete(obj)
        db.commit()
        
        return {"message": f"Obj '{dtgs}' deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

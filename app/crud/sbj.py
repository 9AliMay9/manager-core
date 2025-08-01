from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app import models, schemas


def read_all_sbjs(db: Session) -> list[schemas.SbjListOut]:
    """Return all Sbj entries with related Obj dtgs"""
    try:
        sbjs = db.query(models.Sbj).options(selectinload(models.Sbj.objs)).all()
        return [
            schemas.SbjListOut.model_validate({
                **sbj.__dict__,
                "obj_dtgs": [obj.dtgs for obj in sbj.objs]
                })
                for sbj in sbjs
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def read_sbj_by_dtgs(db: Session, dtgs: str) -> schemas.SbjDetailOut:
    """Return a specific Sbj by its dtgs, including related Obj details"""
    try:
        sbj = (
            db.query(models.Sbj)
            .filter(models.Sbj.dtgs == dtgs)
            .options(selectinload(models.Sbj.objs))
            .first()
        )
        if not sbj:
            raise HTTPException(status_code=404, detail="Sbj not found")
        
        return schemas.SbjDetailOut.model_validate({
            **sbj.__dict__,
            "obj_list": [{"dtgs": o.dtgs, "ctgr": o.ctgr} for o in sbj.objs]
        })
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def read_sbjs_by_ctgr(db: Session, ctgr: str) -> list[schemas.SbjBriefOut]:
    """Return brief list of Sbjs by category"""
    try:
        sbjs = db.query(models.Sbj.dtgs).filter(models.Sbj.ctgr == ctgr).all()
        return [schemas.SbjBriefOut(dtgs=row[0]) for row in sbjs]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def create_sbj(db: Session, sbj_in: schemas.SbjCreate) -> schemas.SbjDetailOut:
    """Create a new Sbj, checking for duplicate dtgs and ctgr_b"""
    try:
        if db.query(models.Sbj).filter(models.Sbj.dtgs == sbj_in.dtgs).first():
            raise HTTPException(status_code=400, detail="Sbj with dtgs already exists")
        if db.query(models.Sbj).filter(models.Sbj.ctgr_b == sbj_in.ctgr_b).first():
            raise HTTPException(status_code=400, detail="ctgr_b already used by another Sbj")

        sbj = models.Sbj(**sbj_in.model_dump())
        db.add(sbj)
        db.commit()
        db.refresh(sbj)
        
        return schemas.SbjDetailOut.model_validate({**sbj.__dict__, "obj_list": []})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def update_sbj(db: Session, dtgs: str, sbj_in: schemas.SbjUpdate) -> schemas.SbjDetailOut:
    """Update dst and ctgr of existing Sbj, return updated details"""
    try:
        sbj = db.query(models.Sbj).filter(models.Sbj.dtgs == dtgs).first()
        if not sbj:
            raise HTTPException(status_code=404, detail="Sbj not found")

        if sbj.dst == sbj_in.dst and sbj.ctgr == sbj_in.ctgr:
            raise HTTPException(status_code=400, detail="No change detected")
    
        sbj.dst = sbj_in.dst
        sbj.ctgr = sbj_in.ctgr
        db.commit()
        db.refresh(sbj)

        objs = (db.query(models.Obj.dtgs, models.Obj.ctgr).filter(models.Obj.ctgr_b == sbj.ctgr_b).all())
        obj_list = [{"dtgs": o[0], "ctgr": o[1]} for o in objs]
        
        return schemas.SbjDetailOut.model_validate({**sbj.__dict__, "obj_list": obj_list,})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def delete_sbj(db: Session, dtgs: str) -> dict:
    """Delete an Sbj unless associated Obj(s) exist"""
    try:
        sbj = db.query(models.Sbj).filter(models.Sbj.dtgs == dtgs).first()
        if not sbj:
            raise HTTPException(status_code=404, detail="Sbj not found")

        linked_objs = db.query(models.Obj).filter(models.Obj.ctgr_b == sbj.ctgr_b).count()        
        if linked_objs > 0:
            raise HTTPException(status_code=400, detail="Cannot delete Sbj: associated Obj(s) exist")

        db.delete(sbj)
        db.commit()
        return {"message": f"Sbj '{dtgs}' deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

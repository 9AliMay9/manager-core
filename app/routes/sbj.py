from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/sbj", tags=["Sbj"])


# Get all Sbj entries with their dtgs and ctgr_b
@router.get("/", response_model=list[schemas.SbjListOut])
def read_all_sbjs(db: Session = Depends(get_db)):
    return crud.sbj.read_all_sbjs(db)


# Get a Sbj by dtgs, including related Objs via some ctgr_b
@router.get("/by-dtgs/{dtgs}", response_model=schemas.SbjDetailOut)
def read_sbj_by_dtgs(dtgs: str, db: Session = Depends(get_db)):
    return crud.sbj.read_sbj_by_dtgs(db, dtgs)


# Get all Sbj entries with a given ctgr
@router.get("/by-ctgr/", response_model=list[schemas.SbjBriefOut])
def read_sbjs_by_ctgr(ctgr: str = Query(...), db: Session = Depends(get_db)):
    return crud.sbj.read_sbjs_by_ctgr(db, ctgr)


# Create a new Sbj entry
@router.post("/", response_model=schemas.SbjDetailOut)
def create_sbj(sbj_in: schemas.SbjCreate, db: Session = Depends(get_db)):
    return crud.sbj.create_sbj(db, sbj_in)


# Update a Sbj by dtgs, only if new values differ
@router.put("/{dtgs}", response_model=schemas.SbjDetailOut)
def update_sbj(dtgs: str, sbj_in: schemas.SbjUpdate, db: Session= Depends(get_db)):
    return crud.sbj.update_sbj(db, dtgs, sbj_in)


# Delete a Sbj by dtgs if no Obj is related
@router.delete("/{dtgs}")
def delete_sbj(dtgs: str, db: Session = Depends(get_db)):
    return crud.sbj.delete_sbj(db, dtgs)

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/obj", tags=["Obj"])


# Get all Obj entries (only dtgs)
@router.get("/", response_model=list[schemas.ObjListOut])
def read_all_objs(db: Session = Depends(get_db)):
    return crud.obj.read_all_objs(db)


# Get an Obj by dtgs, including related Sbj
@router.get("/by-dtgs/{dtgs}", response_model=schemas.ObjDetailOut)
def read_obj_by_dtgs(dtgs: str, db: Session = Depends(get_db)):
    return crud.obj.read_obj_by_dtgs(db, dtgs)


# Get all Obj entries with a given ctgr
@router.get("/by-ctgr/", response_model=list[schemas.ObjListOut])
def read_objs_by_ctgr(ctgr: str = Query(...), db: Session = Depends(get_db)):
    return crud.obj.read_objs_by_ctgr(db, ctgr)


# Create a new Obj entry
@router.post("/", response_model=schemas.ObjDetailOut)
def create_obj(obj_in: schemas.ObjCreate, db: Session = Depends(get_db)):
    return crud.obj.create_obj(db, obj_in)


# Update an Obj by dtgs, only if new values differ
@router.put("/{dtgs}", response_model=schemas.ObjDetailOut)
def update_obj(dtgs: str, obj_in: schemas.ObjUpdate, db: Session = Depends(get_db)):
    return crud.obj.update_obj(db, dtgs, obj_in)


# Delete an Obj by dtgs
@router.delete("/{dtgs}")
def delete_obj(dtgs: str, db: Session = Depends(get_db)):
    return crud.obj.delete_obj(db, dtgs)

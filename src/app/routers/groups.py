from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.group import Group
from ..schemas.group import GroupCreate, GroupResponse

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    new_group = Group(
        name=group.name,
        description=group.description
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("/", response_model=List[GroupResponse])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups


@router.get("/{group_id}", response_model=GroupResponse)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

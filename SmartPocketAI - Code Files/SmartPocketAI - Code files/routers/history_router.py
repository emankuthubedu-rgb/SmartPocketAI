from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import HistoryEntry, User
from schemas import HistoryCreate

router = APIRouter(prefix="/history", tags=["history"])


def serialize(entry: HistoryEntry):
    return {
        "id": entry.id,
        "type": entry.type,
        "title": entry.title,
        "input": entry.input,
        "result": entry.result,
        "createdAt": entry.created_at.isoformat(),
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_history(body: HistoryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = HistoryEntry(user_id=user.id, **body.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return serialize(entry)


@router.get("")
def list_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entries = db.query(HistoryEntry).filter(HistoryEntry.user_id == user.id).order_by(HistoryEntry.created_at.desc()).all()
    return [serialize(entry) for entry in entries]


@router.delete("/{entry_id}")
def delete_history(entry_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.query(HistoryEntry).filter(HistoryEntry.id == entry_id, HistoryEntry.user_id == user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found.")
    db.delete(entry)
    db.commit()
    return {"message": "History entry deleted."}


@router.delete("")
def clear_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = db.query(HistoryEntry).filter(HistoryEntry.user_id == user.id).delete(synchronize_session=False)
    db.commit()
    return {"message": "All history entries cleared.", "deleted": deleted}

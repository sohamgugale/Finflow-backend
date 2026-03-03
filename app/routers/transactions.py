from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=List[schemas.TransactionOut])
def get_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).order_by(models.Transaction.date.desc()).all()

@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_txn = models.Transaction(**txn.dict(), user_id=current_user.id)
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

@router.delete("/{txn_id}")
def delete_transaction(txn_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    txn = db.query(models.Transaction).filter(
        models.Transaction.id == txn_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(txn)
    db.commit()
    return {"message": "Deleted"}

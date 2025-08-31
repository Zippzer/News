from sqlalchemy.orm import Session
from models import POST
from fastapi import HTTPException


def create_post(db: Session, post_data:dict):
    db_post = POST(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_all_post(db: Session):
    return db.query(POST).all()


def get_one_post(db:Session, post_id:int):
    return db.query(POST).filter(POST.id == post_id).first()


def update_post(db:Session, post_id:int, post_data:dict):
    db_item = get_one_post(db,post_id)
    if db_item is None:
        return None
    for key, value in post_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_post(db: Session, post_id: int):
    post = db.query(POST).filter(POST.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"status": "deleted"}

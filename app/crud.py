from sqlalchemy.orm import Session
from models import POST
from schemas import Posts,UpdatePost


def create_post(db:Session,post:Posts):
    db_post = POST(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_all_post(db:Session):
    return db.query(POST).all()


def get_one_post(db:Session,post_id:int):
    return db.query(POST).filter(POST.id == post_id).first()


def update_post(db:Session,post_id:int,post:UpdatePost):
    db_item = get_one_post(db,post_id)
    if db_item  is None:
        return None
    for key, value in post.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    return db_item


def delete_post(db:Session,post_id:int):
    post = db.query(POST).filter(POST.id == post_id).first()
    if post is None:
        return None
    db.delete(post)
    db.commit()
    return None
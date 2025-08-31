from fastapi import APIRouter, Depends
from crud import get_all_post, get_one_post, create_post, update_post,delete_post
from database import get_db
from sqlalchemy.orm import Session
from schemas import UpdatePost,Posts

router = APIRouter()


@router.get("/")
async def get_all(db: Session = Depends(get_db)):
    return get_all_post(db)


@router.get("/{post_id}")
async def get_one(post_id:int, db: Session = Depends(get_db)):
    return get_one_post(db, post_id)


@router.post("/create")
async def create_post_endpoint(post:Posts, db: Session = Depends(get_db)):
    return create_post(db, post.dict())


@router.put("/update/{post_id}")
async def up_post(post_id: int, post: UpdatePost, db: Session = Depends(get_db)):
    return update_post(db, post_id, post.dict(exclude_unset=True))


@router.delete("/delete/{post_id}")
async def del_post(post_id: int, db: Session = Depends(get_db)):
    return delete_post(db, post_id)



# routes.py
from fastapi import APIRouter, HTTPException
from .database import db
from .models import BlogPost
import datetime
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@router.post("/posts/", response_model=BlogPost)
async def create_post(post: BlogPost):
    post_dict = post.dict()
    post_dict['created_at'] = datetime.datetime.utcnow().isoformat()
    result = await db.posts.insert_one(post_dict)
    post_dict['_id'] = str(result.inserted_id)
    return post_dict

@router.get("/posts/{post_id}", response_model=BlogPost)
async def read_post(post_id: str):
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if post is not None:
        return serialize_doc(post)
    raise HTTPException(status_code=404, detail="Post not found")

@router.get("/posts/")
async def read_posts():
    posts = await db.posts.find().to_list(1000)
    return [serialize_doc(post) for post in posts]

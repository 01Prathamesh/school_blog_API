# routes.py
import logging
from fastapi import APIRouter, HTTPException
from school_blog.database import db  # type: ignore
from .models import BlogPost
import datetime
from bson import ObjectId

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@router.post("/posts/", response_model=BlogPost)
async def create_post(post: BlogPost):
    post_dict = post.dict()
    post_dict['created_at'] = datetime.datetime.utcnow().isoformat()
    try:
        result = await db.posts.insert_one(post_dict)
        post_dict['_id'] = str(result.inserted_id)
        logger.info(f"Post created with ID: {post_dict['_id']}")
        return post_dict
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/posts/{post_id}", response_model=BlogPost)
async def read_post(post_id: str):
    try:
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        if post is not None:
            return serialize_doc(post)
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        logger.error(f"Error fetching post with ID {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/posts/")
async def read_posts():
    try:
        posts = await db.posts.find().to_list(1000)
        return [serialize_doc(post) for post in posts]
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

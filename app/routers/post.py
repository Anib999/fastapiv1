from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get('/sqlalch', response_model=List[schemas.PostReponse])
@router.get('/sqlalch', response_model=List[schemas.PostOut])
def test_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    print(limit)

    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == user_id.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts  = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.get('/')
def get_posts(user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'message': posts}


@router.post('/')
def create_posts(payload: schemas.Post, status_code=status.HTTP_201_CREATED):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (payload.title, payload.content, payload.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'message': new_post}
# def create_post(payload: dict = Body(...)):
#     return {'message': f"title {payload['title']}"}


@router.post('/sqlpost', status_code=status.HTTP_201_CREATED, response_model=schemas.PostReponse)
def create_alc_post(payload: schemas.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # this is little inefficient
    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.published)

    # this is efficient
    # ** unpacks a dictionary
    new_post = models.Post(owner_id=user_id.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get('/sqlgetone/{id}', response_model=schemas.PostReponse)
@router.get('/sqlgetone/{id}', response_model=schemas.PostOut)
def get_one_post(id: int, response: Response, db: Session = Depends(get_db)):
    # new_psot = db.query(models.Post).filter(models.Post.id == id).first()
    new_psot = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not new_psot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
    return new_psot


@router.get('/{id}')
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts where id = %s""", (str(id),))
    onePost = cursor.fetchone()
    if not onePost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'{id} is not found'}
    return {'message': onePost}


@router.delete('/{id}')
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id} is not found try again.')

    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {'message': 'post successfully deleted'}


@router.delete('/sqldelete/{id}')
def delete_one_post(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT, user_id: int = Depends(oauth2.get_current_user)):
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()


    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id} is not found try again.')

    if deleted_post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not Authorized invalid login')

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_post(id: int, post: schemas.Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
    return {'message': updated_post}


@router.put('/sqlput/{id}')
def update_poster(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    new_post = db.query(models.Post).filter(models.Post.id == id)
    fPost = new_post.first()

    if fPost == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')

    # if new_post.owner_id != oauth2.get_current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not Authorized')

    new_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return new_post.first()

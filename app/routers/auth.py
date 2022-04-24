from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Auth']
)

@router.post('/logins', response_model=schemas.Token)
def loginUser(user_cre: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_cre.username).first()
    # {"username": "asdf", "password": "asdf"} 
    # always changes to username even if email or others
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid username or password')
    
    if not utils.verify(user_cre.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid username or password')
    
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
    # return a token
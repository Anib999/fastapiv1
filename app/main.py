# double check if we are using venv python.exe
# command palet select interpretor .\venv\Scripts\python.exe
# then go to terminal then select activate.bat
# venv\Scripts\activate.bat remove .bat if not working
from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'https://www.google.com'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [
#     {'id': 1, 'title': 'Hello Title', 'content': 'this is content'},
#     {'id': 2, 'title': 'Hello Title 2', 'content': 'this is content 2'}
# ]

# def find_array(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_array(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Hello chicks api"}

@app.get('/login')
def login_usr():
    return {'message': 'Login here'}


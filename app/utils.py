from passlib.context import CryptContext

pwd_con = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    hashed_password = pwd_con.hash(password)
    return hashed_password

def verify(plain, hashed):
    return pwd_con.verify(plain, hashed)
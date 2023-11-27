from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import pymysql

class Item(BaseModel):
    login_or_email: str
    password: str

connection = pymysql.connect(host="tutorino.ddns.net",user="TutorinoAPI",passwd="IOProj2023",database="tutorino")
cursor = connection.cursor()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def is_login_or_email_in_database(login_or_email: str):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login_or_email, login_or_email))
            result = cursor.fetchone()
            return result is not None
    

def validate_login_credentials(login: str, password: str):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE (login = %s OR email = %s) AND password = %s", (login, login, password))
            result = cursor.fetchone()
            return result is not None
    

def create_user_account(login: str, email: str, password: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, email, password) VALUES (%s, %s, %s)", (login, email, password))
            connection.commit()
            return {"message": "User account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/items")
def create_item():
    return "Hello"

@app.post("/login")
async def login(item: Item):
    if not is_login_or_email_in_database(item.login_or_email):
        raise HTTPException(status_code=401, detail="Invalid login or email")

    if not validate_login_credentials(item.login_or_email, item.password):
        raise HTTPException(status_code=401, detail="Invalid password")

@app.post("/register")
async def register(login: str, email: str, password: str):
    if is_login_or_email_in_database(login) or is_login_or_email_in_database(email):
        raise HTTPException(status_code=409, detail="Login or email already exists in the database")

    return create_user_account(login, email, password)


connection.close()
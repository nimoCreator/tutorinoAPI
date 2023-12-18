from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import pymysql
from pydantic import BaseModel
from datetime import date, timedelta, datetime
import jwt
from jwt import PyJWTError
import random

class Item(BaseModel):
    login_or_email: str
    password: str

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


connection = pymysql.connect(host="tutorino.ddns.net",user="TutorinoAPI",passwd="IOProj2023",database="tutorino")
cursor = connection.cursor()

app = FastAPI()

allowed_tables = ["ogloszenie", "operator", "przedmioty", "rating", "reports", "uczen", "users", "wiadomosci", "korepetytor", "korepetycje","czlonkowie_konwersacji","konwersacje","seen_by"]

def get_table_data(table_name: str):
    if table_name not in allowed_tables:
        raise HTTPException(status_code=404, detail="Table not found")

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()
            return table_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_korepetytor_profile(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM korepetytor WHERE uuid = {user_id}")
            korepetytor_data = cursor.fetchone()
            if korepetytor_data:
                cursor.execute(f"SELECT * FROM ogloszenia WHERE kuid = {korepetytor_data[0]}")
                korepetytor_ogloszenia = cursor.fetchall()
                cursor.execute(f"SELECT * FROM rating WHERE recipient = {korepetytor_data[0]}")
                oceny_korepetytora = cursor.fetchall()
                return korepetytor_data, korepetytor_ogloszenia, oceny_korepetytora
            else:
                raise HTTPException(status_code=404, detail="Korepetytor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_konwersacja(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM konwersacje WHERE owner = {user_id}")

            konwersacja_data = cursor.fetchall()
            return konwersacja_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_wiadomosci(konwersacja_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM messages WHERE konferencja = {konwersacja_id}")
            wiadomosci_data = cursor.fetchall()
            return wiadomosci_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_korepetycje_by_uczen(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM korepetycje WHERE uczen = {user_id}")
            korepetycje_data = cursor.fetchall()
            return korepetycje_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_korepetycje_by_korepetytor(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM korepetycje WHERE korepetytor = {user_id}")
            korepetycje_data = cursor.fetchall()
            return korepetycje_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def is_login_or_email_in_database(login_or_email: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login_or_email, login_or_email))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def validate_login_credentials(login: str, password: str):
    try:    
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE (login = %s OR email = %s) AND password = %s", (login, login, password))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def validate_session_inbase(id: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE sessionid = %s", (id))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def create_user_account(login: str, email: str, password: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, email, password) VALUES (%s, %s, %s)", (login, email, password))
            connection.commit()
            return {"message": "User account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
def add_new_session(userID: str):
    try:
        with connection.cursor() as cursor:
            valid_from = str(date.today())
            today = date.today()
            td = timedelta(days=1)
            valid_until = str(today + td)
            sessionId = str(random.randint(10000000000,99999999999))
            cursor.execute("INSERT INTO sessions (sessionId, user_uuid, valid_from, valid_until, session_key) VALUES (%s, %s, %s, %s)", (sessionId, userID, valid_from, valid_until))
            connection.commit()
            return {"sessionId":sessionId}
    except pymysql.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        session_id: str = payload.get("sub")
        if session_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if not validate_session_inbase(session_id):
        raise HTTPException(status_code=401, detail="Session ID wrong or expired")

    return session_id

@app.post("/login")
def login(item: Item):
    if not is_login_or_email_in_database(item.login_or_email):
        raise HTTPException(status_code=401, detail="Invalid login or email")

    if not validate_login_credentials(item.login_or_email, item.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    session_id = add_new_session(item.login_or_email)["sessionId"]
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": session_id}, expires_delta=expires_delta)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
def register(login: str, email: str, password: str):
    if is_login_or_email_in_database(login) or is_login_or_email_in_database(email):
        raise HTTPException(status_code=409, detail="Login or email already exists in the database")

    # Create a new user account and return the access token
    user_id = create_user_account(login, email, password)
    session_id = add_new_session(user_id)["sessionId"]
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": session_id}, expires_delta=expires_delta)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/validateSession")
def sessionGet(sessionID: str):
    if not validate_session_inbase(sessionID):
        raise HTTPException(status_code=409, detail="Session ID wrong or expired")

    return {"message": "session valid"}

@app.post("/addSession")
def sessionAdd(userID: str):
    result = add_new_session(userID)
    if "sessionId" in result:
        return {"sessionId": result["sessionId"]}
    else:
        raise HTTPException(status_code=409, detail="Failed to add new session")
    

@app.get("/")
async def hello():
    return "Hello"

@app.get("/ogloszenie")
async def get_ogloszenie():
    return get_table_data("ogloszenie")

@app.get("/operator")
async def get_operator():
    return get_table_data("operator")

@app.get("/przedmioty")
async def get_przedmioty():
    return get_table_data("przedmioty")

@app.get("/rating")
async def get_rating():
    return get_table_data("rating")

@app.get("/reports")
async def get_reports():
    return get_table_data("reports")

@app.get("/uczen")
async def get_uczen():
    return get_table_data("uczen")

@app.get("/users")
async def get_users():
    return get_table_data("users")

@app.get("/wiadomosci")
async def get_wiadomosci():
    return get_table_data("wiadomosci")

@app.get("/korepetytor")
async def get_korepetytor():
    return get_table_data("korepetytor")

@app.get("/korepetycje")
async def get_korepetycje():
    return get_table_data("korepetycje")

@app.get("/seen_by")
async def get_ogloszenie():
    return get_table_data("seen_by")

@app.get("/konwersacje")
async def get_ogloszenie():
    return get_table_data("konwersacje")

@app.get("/czlonkowie_konwersacji")
async def get_ogloszenie():
    return get_table_data("czlonkowie_konwersacji")

@app.get("/korepetytor_profile/{user_id}")
async def get_korepetytor_profile(user_id: int):
    return get_korepetytor_profile(user_id)

@app.get("/konwersacje/{user_id}")
async def get_konwersacje_uzytkownika(user_id: int):
    return get_konwersacja(user_id)

@app.get("/wiadomosci/{conversation_id}")
async def get_wiadomosci_konwersacji(conversation_id: int):
    return get_wiadomosci(conversation_id)

@app.get("/korepetycje_k/{user_id}")
async def get_korepetytor_korepetycje(user_id: int):
    return get_korepetycje_by_korepetytor(user_id)

@app.get("/korepetycje_u/{user_id}")
async def get_uczen_korepetycje(user_id: int):
    return get_korepetycje_by_uczen(user_id)

@app.on_event("shutdown")
async def shutdown_event():
    connection.close()
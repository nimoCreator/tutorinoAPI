from fastapi import FastAPI, HTTPException
import pymysql
from pydantic import BaseModel

class Item(BaseModel):
    login_or_email: str
    password: str

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
    

def create_user_account(login: str, email: str, password: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, email, password) VALUES (%s, %s, %s)", (login, email, password))
            connection.commit()
            return {"message": "User account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login(item: Item):
    if not is_login_or_email_in_database(item.login_or_email):
        raise HTTPException(status_code=401, detail="Invalid login or email")

    if not validate_login_credentials(item.login_or_email, item.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return {"message": "login success"}

@app.post("/register")
def register(login: str, email: str, password: str):
    if is_login_or_email_in_database(login) or is_login_or_email_in_database(email):
        raise HTTPException(status_code=409, detail="Login or email already exists in the database")

    return create_user_account(login, email, password)

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
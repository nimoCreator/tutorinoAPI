from flask import Flask, request, jsonify
import pymysql
from datetime import date, timedelta, datetime
import jwt
import random
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

connection = pymysql.connect(host="tutorino.ddns.net", user="TutorinoAPI", passwd="IOProj2023", database="tutorino")
cursor = connection.cursor()

allowed_tables = ["ogloszenie", "operator", "przedmioty", "rating", "reports", "uczen", "users", "wiadomosci", "korepetytor", "korepetycje","czlonkowie_konwersacji","konwersacje","seen_by"]

def get_table_data(table_name: str):
    if table_name not in allowed_tables:
        return jsonify({"error": "Table not found"}), 404

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()
            return table_data
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
                return jsonify({"error": "Korepetytor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_konwersacja(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM konwersacje WHERE owner = {user_id}")

            konwersacja_data = cursor.fetchall()
            return konwersacja_data
    except Exception as e:
         return jsonify({"error": str(e)}), 500

def get_wiadomosci(konwersacja_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM messages WHERE konferencja = {konwersacja_id}")
            wiadomosci_data = cursor.fetchall()
            return wiadomosci_data
    except Exception as e:
         return jsonify({"error": str(e)}), 500

def get_korepetycje_by_uczen(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM korepetycje WHERE uczen = {user_id}")
            korepetycje_data = cursor.fetchall()
            return korepetycje_data
    except Exception as e:
         return jsonify({"error": str(e)}), 500

def get_korepetycje_by_korepetytor(user_id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM korepetycje WHERE korepetytor = {user_id}")
            korepetycje_data = cursor.fetchall()
            return korepetycje_data
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    
def is_login_or_email_in_database(login_or_email: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login_or_email, login_or_email))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    

def validate_login_credentials(login: str, password: str):
    try:    
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE (login = %s OR email = %s) AND password = %s", (login, login, password))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    
def validate_session_inbase(id: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sessions WHERE sessionid = %s", (id))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    

def create_user_account(login: str, email: str, password: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, email, password) VALUES (%s, %s, %s)", (login, email, password))
            connection.commit()
            return {"message": "User account created successfully"}
    except Exception as e:
         return jsonify({"error": str(e)}), 500
   
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
         return jsonify({"error": str(e)}), 500

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token():
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    
    credentials_exception = Unauthorized("Invalid credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        session_id = payload.get("sub")
        if session_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    if not validate_session_inbase(session_id):
        raise Unauthorized("Session ID wrong or expired")

    return session_id

def getOffers(uuid, session_id):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM sessions WHERE user_uuid=? AND session_id=?", (uuid, session_id))
        result = cursor.fetchone()

        if result:
            get_korepetycje_by_uczen(uuid)
        else:
            return jsonify({"detail": "No results"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/getOffers",methods=["GET"])
def getMyOffers():
    session_id = request.args.get("sessionID")
    userId = request.args.get("userID")
    if not validate_session_inbase(session_id):
        return jsonify({"error": "Session ID expired"}), 409
    getOffers(userId,session_id)
    

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    login_or_email = data.get("login_or_email")
    password = data.get("password")

    if not is_login_or_email_in_database(login_or_email):
        return jsonify({"detail": "Invalid login or email"}), 401

    if not validate_login_credentials(login_or_email, password):
        return jsonify({"detail": "Invalid password"}), 401

    session_id = add_new_session(login_or_email)["sessionId"]
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": session_id}, expires_delta=expires_delta)

    return jsonify({"access_token": access_token, "token_type": "bearer"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    login = data.get("login")
    email = data.get("email")
    password = data.get("password")

    if is_login_or_email_in_database(login) or is_login_or_email_in_database(email):
        return jsonify({"error": "Login or email already exists in the database"}), 409

    user_id = create_user_account(login, email, password)
    session_id = add_new_session(user_id)["sessionId"]
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": session_id}, expires_delta=expires_delta)

    return {"access_token": access_token, "token_type": "bearer"}

@app.route("/validateSession", methods=["GET"])
def session_get():
    session_id = request.args.get("sessionID")
    if not validate_session_inbase(session_id):
        return jsonify({"error": "Session ID wrong or expired"}), 409

    return {"message": "session valid"}

@app.route("/addSession", methods=["POST"])
def session_add():
    data = request.json
    user_id = data.get("userID")

    result = add_new_session(user_id)
    if "sessionId" in result:
        return {"sessionId": result["sessionId"]}
    else:
        return jsonify({"error": "Failed to add new session"}), 409
    
@app.route("/")
def hello():
    return "Hello"

@app.route("/ogloszenie")
def get_ogloszenie():
    return jsonify(get_table_data("ogloszenie"))

@app.route("/operator")
def get_operator():
    return jsonify(get_table_data("operator"))

@app.route("/przedmioty")
def get_przedmioty():
    return jsonify(get_table_data("przedmioty"))

@app.route("/rating")
def get_rating():
    return jsonify(get_table_data("rating"))

@app.route("/reports")
def get_reports():
    return jsonify(get_table_data("reports"))

@app.route("/uczen")
def get_uczen():
    return jsonify(get_table_data("uczen"))

@app.route("/users")
def get_users():
    return jsonify(get_table_data("users"))

@app.route("/wiadomosci")
def get_wiadomosci():
    return jsonify(get_table_data("wiadomosci"))

@app.route("/korepetytor")
def get_korepetytor():
    return jsonify(get_table_data("korepetytor"))

@app.route("/korepetycje")
def get_korepetycje():
    return jsonify(get_table_data("korepetycje"))

@app.route("/seen_by")
def get_seen_by():
    return jsonify(get_table_data("seen_by"))

@app.route("/konwersacje")
def get_konwersacje():
    return jsonify(get_table_data("konwersacje"))

@app.route("/czlonkowie_konwersacji")
def get_czlonkowie_konwersacji():
    return jsonify(get_table_data("czlonkowie_konwersacji"))

@app.route("/korepetytor_profile/<int:user_id>")
def get_korepetytor_profile(user_id):
    return jsonify(get_korepetytor_profile(user_id))

@app.route("/konwersacje/<int:user_id>")
def get_konwersacje_uzytkownika(user_id):
    return jsonify(get_konwersacja(user_id))

@app.route("/wiadomosci/<int:conversation_id>")
def get_wiadomosci_konwersacji(conversation_id):
    return jsonify(get_wiadomosci(conversation_id))

@app.route("/korepetycje_k/<int:user_id>")
def get_korepetytor_korepetycje(user_id):
    return jsonify(get_korepetycje_by_korepetytor(user_id))

@app.route("/korepetycje_u/<int:user_id>")
def get_uczen_korepetycje(user_id):
    return jsonify(get_korepetycje_by_uczen(user_id))

@app.route("/shutdown")
def shutdown_event():
    connection.close()
    return "Server shutting down..."

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5555)
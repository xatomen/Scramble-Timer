from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter()

# Seguridad

# Configuración para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para firmar los tokens
SECRET_KEY = "jorge123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para obtener el usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        db_user = db.query(User).filter(User.username == username).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return db_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------------------------------


# Operaciones CRUD para la tabla User

# Definimos un modelo para la creación de instancias de User
class UserBase(BaseModel):
    name: str
    username: str
    password: str
    email: str

# Enpoint POST para crear un nuevo usuario
@router.post("/user/", tags=["User"])
def post_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return {"error": "Username already registered"}
    # Hashear la contraseña antes de guardarla
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

# Definimos un endpoint GET en la ruta "/user/{id}"
@router.get("/user/{id}", tags=["User"])
def get_user(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de User con el id proporcionado
    db_user = db.query(User).filter(User.id_user == id).first()
    # Devolvemos la instancia de User
    return db_user

# Definimos un endpoint GET en la ruta "/user/"
@router.get("/user/", tags=["User"])
def get_users(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de User
    db_users = db.query(User).all()
    # Devolvemos la lista de instancias de User
    return db_users

# Definimos un endpoint DELETE en la ruta "/user/{id}"
@router.delete("/user/{id}", tags=["User"])
def delete_user(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de User con el id proporcionado
    db_user = db.query(User).filter(User.id_user == id).first()
    # Eliminamos la instancia de User de la sesión de la base de datos
    db.delete(db_user)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de User eliminada
    return db_user

# Definimos un endpoint PUT en la ruta "/user/{id}"
@router.put("/user/{id}", tags=["User"])
def put_user(id: int, user: UserBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de User con el id proporcionado
    db_user = db.query(User).filter(User.id_user == id).first()
    # Actualizamos los campos de la instancia de User con los valores proporcionados
    db_user.name = user.name
    db_user.username = user.username
    db_user.password = user.password
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de User para obtener los datos actualizados desde la base de datos
    db.refresh(db_user)
    # Devolvemos la instancia de User actual
    return db_user

# Endpoint para iniciar sesión
@router.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    # Crear un token de acceso
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Ejemplo de ruta protegida
@router.get("/protected-route", tags=["Auth"])
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
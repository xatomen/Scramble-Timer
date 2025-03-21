from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User

router = APIRouter()

# Operaciones CRUD para la tabla User

# Definimos un modelo para la creación de instancias de User
class UserBase(BaseModel):
    name: str
    username: str
    password: str

# Definimos un endpoint POST en la ruta "/user/"
@router.post("/user/", tags=["User"])
def post_user(user: UserBase, db: Session = Depends(get_db)):
    # Verificamos si el usuario ya existe por username
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return {"error": "Username already registered"}
    # Convertimos el modelo de pydantic a una instancia de la clase User de SQLAlchemy
    db_user = User(**user.dict())
    # Añadimos la nueva instancia de User a la sesión de la base de datos
    db.add(db_user)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de User para obtener los datos actualizados desde la base de datos
    db.refresh(db_user)
    # Devolvemos la instancia de User creada
    return user

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
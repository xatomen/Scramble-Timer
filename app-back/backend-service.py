# Servicio backend para la aplicación utilizando FastAPI

# Importamos fastapi
from fastapi import FastAPI, Depends

# Importamos sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Inicialización de la aplicación
app = FastAPI()

# Configuración de la base de datos mysql
from config import user, password, host, port, db_name
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Definición de las tablas de la base de datos

class Cube(Base):
    __tablename__ = 'cube'
    id_cube = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50))
    model = Column(String(50))
    fk_cube_type = Column(Integer, ForeignKey('cube_type.id_cube_type'))
    magnetic = Column(Boolean)

class Solve(Base):
    __tablename__ = 'solve'
    id_solve = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    time = Column(Time)
    scramble = Column(String(100))
    fk_cube = Column(Integer, ForeignKey('cube.id_cube'))
    fk_solve_type = Column(Integer, ForeignKey('solve_type.id_solve_type'))

class Session(Base):
    __tablename__ = 'session'
    id_session = Column(Integer, primary_key=True, index=True)
    name = Column(Integer)
    avg = Column(Integer)
    ao5 = Column(Integer)
    ao12 = Column(Integer)
    qty = Column(Integer)
    fk_solve = Column(Integer, ForeignKey('solve.id_solve'))
    fk_user = Column(Integer, ForeignKey('user.id_user'))

class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(Integer)
    username = Column(Integer)
    password = Column(Integer)

class CubeType(Base):
    __tablename__ = 'cube_type'
    id_cube_type = Column(Integer, primary_key=True, index=True)
    cube_type = Column(String(50))

class SolveType(Base):
    __tablename__ = 'solve_type'
    id_solve_type = Column(Integer, primary_key=True, index=True)
    solve_type = Column(String(50))

# # Crear las tablas en la base de datos si no existen
# Base.metadata.create_all(bind=engine)

from pydantic import BaseModel
from datetime import datetime, time

class SolveCreate(BaseModel):
    date: datetime
    time: time
    scramble: str
    fk_cube: int
    fk_solve_type: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definimos un endpoint POST en la ruta "/solve/"
@app.post("/solve/")
def post_solve(solve: SolveCreate, db: Session = Depends(get_db)):
    # Convertimos el objeto SolveCreate en un diccionario y lo desempaquetamos para crear una instancia de Solve
    db_solve = Solve(**solve.dict())
    # Añadimos la nueva instancia de Solve a la sesión de la base de datos
    db.add(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve creada
    return db_solve

# Definimos un endpoint GET en la ruta "/solve/{id}"
@app.get("/solve/{id}")
def get_solve(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Devolvemos la instancia de Solve
    return db_solve

# Definimos un endpoint GET en la ruta "/solve/"
@app.get("/solve/")
def get_solves(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de Solve
    db_solves = db.query(Solve).all()
    # Devolvemos la lista de instancias de Solve
    return db_solves

# Definimos un endpoint DELETE en la ruta "/solve/{id}"
@app.delete("/solve/{id}")
def delete_solve(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Eliminamos la instancia de Solve de la sesión de la base de datos
    db.delete(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Solve eliminada
    return db_solve

# Definimos un endpoint PUT en la ruta "/solve/{id}"
@app.put("/solve/{id}")
def put_solve(id: int, solve: SolveCreate, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Actualizamos los campos de la instancia de Solve con los valores proporcionados
    db_solve.date = solve.date
    db_solve.time = solve.time
    db_solve.scramble = solve.scramble
    db_solve.fk_cube = solve.fk_cube
    db_solve.fk_solve_type = solve.fk_solve_type
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve actualizada
    return

# Definimos un endpoint POST en la ruta "/cube/"
@app.post("/cube/")
def post_cube(cube: Cube, db: Session = Depends(get_db)):
    # Añadimos la nueva instancia de Cube a la sesión de la base de datos
    db.add(cube)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Cube para obtener los datos actualizados desde la base de datos
    db.refresh(cube)
    # Devolvemos la instancia de Cube creada
    return cube

# Definimos un endpoint GET en la ruta "/cube/{id}"
@app.get("/cube/{id}")
def get_cube(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Cube con el id proporcionado
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    # Devolvemos la instancia de Cube
    return db_cube

# Definimos un endpoint GET en la ruta "/cube/"
@app.get("/cube/")
def get_cubes(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de Cube
    db_cubes = db.query(Cube).all()
    # Devolvemos la lista de instancias de Cube
    return db_cubes

# Definimos un endpoint DELETE en la ruta "/cube/{id}"
@app.delete("/cube/{id}")
def delete_cube(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Cube con el id proporcionado
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    # Eliminamos la instancia de Cube de la sesión de la base de datos
    db.delete(db_cube)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Cube eliminada
    return db_cube

# Definimos un endpoint PUT en la ruta "/cube/{id}"
@app.put("/cube/{id}")
def put_cube(id: int, cube: Cube, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Cube con el id proporcionado
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    # Actualizamos los campos de la instancia de Cube con los valores proporcionados
    db_cube.brand = cube.brand
    db_cube.model = cube.model
    db_cube.fk_cube_type = cube.fk_cube_type
    db_cube.magnetic = cube.magnetic
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Cube para obtener los datos actualizados desde la base de datos
    db.refresh(db_cube)
    # Devolvemos la instancia de Cube actualizada
    return db_cube

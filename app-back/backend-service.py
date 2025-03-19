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




from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Criação da aplicação FastAPI
app = FastAPI()

# Configuração do Banco de Dados
DATABASE_URL = "sqlite:///./test.db"  # Define o caminho para o banco de dados SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Produto para o banco de dados
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

# Criando as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Modelo Pydantic para os dados recebidos pela API
class Product(BaseModel):
    name: str
    description: str
    price: float
    category: str

    class Config:
        orm_mode = True  # Para permitir conversão automática para o modelo ORM

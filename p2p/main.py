# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import crud, schemas, models
from product import Product, ProductDB
from auth import create_access_token, verify_password

app = FastAPI()
products = []
# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello, World"}

@app.post("/products/", response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = ProductDB(name=product.name, description=product.description, price=product.price, category=product.category)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)  # Atualiza o objeto para obter o ID do banco de dados
    return db_product

@app.get("/products/", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}



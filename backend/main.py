from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Product                      # Pydantic model
import database_models                          # SQLAlchemy model
from database import get_db, engine, Base       # DB config
from fastapi.middleware.cors import CORSMiddleware

#  Create tables in MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

#  CREATE PRODUCT
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Product created successfully",
            "data": {
                "id": db_product.id,
                "name": db_product.name,
                "description": db_product.description,
                "price": db_product.price,
                "quantity": db_product.quantity,
            }
        }
    )


#  GET ALL PRODUCTS
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(database_models.Product).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Products fetched successfully",
            "data": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "price": p.price,
                    "quantity": p.quantity,
                } for p in products
            ]
        }
    )


#  GET PRODUCT BY ID
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Product fetched successfully",
            "data": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
            }
        }
    )


# UPDATE PRODUCT
@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # update fields
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Product updated successfully",
            "data": {
                "id": db_product.id,
                "name": db_product.name,
                "description": db_product.description,
                "price": db_product.price,
                "quantity": db_product.quantity,
            }
        }
    )


# DELETE PRODUCT
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(db_product)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Product deleted successfully"
        }
    )
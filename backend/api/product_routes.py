from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.database import get_db
from core.auth import get_current_user
from models.product import Product
from repository import product_repo

router = APIRouter()


# CREATE PRODUCT
@router.post("/products")
def create(
    product: Product,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_product = product_repo.create_product(db, product)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
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


# GET ALL PRODUCTS
@router.get("/products")
def get_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    products = product_repo.get_all_products(db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Products fetched successfully",
            "data": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "price": p.price,
                    "quantity": p.quantity,
                }
                for p in products
            ]
        }
    )


# GET PRODUCT BY ID
@router.get("/products/{id}")
def get_one(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = product_repo.get_product(db, id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
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
@router.put("/products/{id}")
def update(
    id: int,
    updated_product: Product,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = product_repo.get_product(db, id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    updated = product_repo.update_product(db, product, updated_product)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Product updated successfully",
            "data": {
                "id": updated.id,
                "name": updated.name,
                "description": updated.description,
                "price": updated.price,
                "quantity": updated.quantity,
            }
        }
    )


# DELETE PRODUCT
@router.delete("/products/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = product_repo.get_product(db, id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product_repo.delete_product(db, product)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Product deleted successfully"
        }
    )
from db import models

def create_product(db, product):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_products(db):
    return db.query(models.Product).all()


def get_product(db, id):
    return db.query(models.Product).filter(models.Product.id == id).first()


def delete_product(db, product):
    db.delete(product)
    db.commit()
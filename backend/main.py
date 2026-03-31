from fastapi import FastAPI
from db.database import engine, Base
from api.v1 import product_routes as v1_products
from api.v1 import auth_routes as v1_auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

# V1 Routes
app.include_router(v1_auth.router,     prefix="/api/v1", tags=["v1 - Auth"])
app.include_router(v1_products.router, prefix="/api/v1")
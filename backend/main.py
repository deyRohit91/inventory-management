from fastapi import FastAPI
from db.database import engine, Base
from api import auth_routes, product_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(product_routes.router)
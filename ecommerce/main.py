from fastapi import FastAPI
from ecommerce.database import engine
from ecommerce.models import Base
from ecommerce.routes.routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, product as product_api, supplier as supplier_api, chatbot  # Rename imports
from app.core.config import settings
from app.db.database import engine
from app.models import user, product as product_model, supplier as supplier_model  # Keep these for models

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables (Use Alembic for migrations in production)
user.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
supplier_model.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include routers correctly
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(product_api.router, prefix="/products", tags=["products"])  # Use renamed import
app.include_router(supplier_api.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

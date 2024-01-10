from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db import init_db, get_db
from auth import router as auth_router

app = FastAPI()

# Create an instance of the Engine
engine = create_engine("sqlite:///test.db")

# Initialize the database when the app starts
init_db()

# Include routers from other modules
app.include_router(auth_router)

# FastAPI route using dependency injection to get the database session
@app.on_event("shutdown")
def shutdown_event():
    print("Application shutting down")
    engine.dispose()

@app.get("/hello")
async def hello(db: Session = Depends(get_db)):
    return {"message": "Hello, World!"}

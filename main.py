from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="Taskoria API", version="1.0.0")

# CORS for local dev between ports 3000 and 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuoteRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    service: str
    description: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    postcode: Optional[str] = None

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

class ProSignup(BaseModel):
    business_name: str
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None
    category: str
    suburb: Optional[str] = None
    abn: Optional[str] = None
    plan: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": "taskoria", "version": "1.0.0"}

@app.post("/quote")
async def create_quote(payload: QuoteRequest):
    # In a real app, insert into DB and notify providers
    if not payload.service:
        raise HTTPException(status_code=400, detail="Service is required")
    return {
        "success": True,
        "message": "Your request has been received. We'll match you with verified professionals shortly.",
        "data": payload.model_dump(),
    }

@app.post("/contact")
async def contact(payload: ContactRequest):
    return {
        "success": True,
        "message": "Thanks for reaching out. Our team will get back to you within 24 hours.",
        "data": payload.model_dump(),
    }

@app.post("/pro-signup")
async def pro_signup(payload: ProSignup):
    return {
        "success": True,
        "message": "Welcome to Taskoria! Your account is under review for verification.",
        "data": payload.model_dump(),
    }

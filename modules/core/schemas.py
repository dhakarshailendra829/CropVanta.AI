from pydantic import BaseModel, Field
from typing import Optional

class CropInput(BaseModel):
    nitrogen: float = Field(default=50.0, ge=0, le=140)
    phosphorus: float = Field(default=50.0, ge=5, le=145)
    potassium: float = Field(default=50.0, ge=5, le=205)
    temperature: float = Field(default=25.0)
    humidity: float = Field(default=60.0, ge=0, le=100)
    ph: float = Field(default=6.5, ge=0, le=14)
    rainfall: float = Field(default=100.0, ge=0)

class WeatherData(BaseModel):
    city: str
    temp: float
    description: str
    humidity: int
# ---------------------------
# User Schemas (SaaS Layer)
# ---------------------------

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., max_length=150)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

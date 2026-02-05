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
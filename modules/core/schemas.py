from pydantic import BaseModel, Field

class CropInput(BaseModel):
    nitrogen: float = Field(..., ge=0, le=140)
    phosphorus: float = Field(..., ge=5, le=145)
    potassium: float = Field(..., ge=5, le=205)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    ph: float = Field(..., ge=0, le=14)
    rainfall: float = Field(..., ge=0)

class WeatherData(BaseModel):
    city: str
    temp: float
    description: str
    humidity: int
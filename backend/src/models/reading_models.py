from pydantic import BaseModel, Field
from typing import Optional


class ReadingRequest(BaseModel):
    name: str = Field(..., example="TestUser1")
    date: str = Field(..., example="1999-11-13")        # YYYY-MM-DD
    time: str = Field(..., example="16:20:00")          # HH:MM:SS (24h)
    place: str = Field(..., example="Visakhapatnam, India")
    ayanamsa: Optional[str] = Field(default="raman", example="raman")


class ReadingResponse(BaseModel):
    chart_id: str
    report_markdown: str

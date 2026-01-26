from fastapi import FastAPI
from src.models.reading_models import ReadingRequest, ReadingResponse
from src.services.reading_service import generate_reading

app = FastAPI(title="AstroAI API", version="v1")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reading/generate", response_model=ReadingResponse)
def reading_generate(req: ReadingRequest):
    result = generate_reading(
        name=req.name,
        date=req.date,
        time=req.time,
        place=req.place,
        ayanamsa=req.ayanamsa or "raman",
    )
    return result


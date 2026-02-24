from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.models.reading_models import ReadingRequest, ReadingResponse
from src.services.reading_service import generate_reading

app = FastAPI(title="AstroAI API", version="v1")

# ✅ CORS Middleware (for frontend localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reading/generate", response_model=ReadingResponse)
def reading_generate(req: ReadingRequest):
    try:
        result = generate_reading(
            name=req.name,
            date=req.date,
            time=req.time,
            place=req.place,
            ayanamsa=req.ayanamsa or "raman",
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
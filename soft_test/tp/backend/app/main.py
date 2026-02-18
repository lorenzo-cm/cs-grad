from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.main_router import main_router

app = FastAPI(title="Wordle API")

# CORS: Permitir frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

app.include_router(main_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import audit, chat, crystal, inject

app = FastAPI(title="immune-crystal", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(inject.router)
app.include_router(audit.router)
app.include_router(crystal.router)


@app.get("/health")
def health():
    return {"status": "ok", "name": "immune-crystal"}

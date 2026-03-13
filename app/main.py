import uvicorn
from fastapi import FastAPI
from app.api.report_router import router

app = FastAPI(title="Word Frequency Service")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

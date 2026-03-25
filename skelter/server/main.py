import uvicorn
from fastapi import FastAPI
from skelter.server.api.generate import router as generate_router

app = FastAPI(title="Skelter Backend")

app.include_router(generate_router)


@app.get("/")
def root():
    return {"status": "skelter backend running"}


def run_server():
    uvicorn.run("skelter.server.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
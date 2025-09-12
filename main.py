from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    """Health check endpoint for service verification"""
    return "pong"

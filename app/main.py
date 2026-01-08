from fastapi import FastAPI
from app.routers import user

app = FastAPI()
#pip install gunicorn "uvicorn[standard]" for production
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"msg": "Hello World"}
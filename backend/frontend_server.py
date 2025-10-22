from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve HTML/CSS/JS from current folder
app.mount("/", StaticFiles(directory=".", html=True), name="static")

from fastapi import FastAPI
from fastapi.staticfiles  import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT,"frontend")

@app.get("/")
@app.get("/{path:path}")
def spa(path : str = ""):
    return FileResponse(os.path.join(FRONTEND_DIR,"index.html"))
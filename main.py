from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.middlewares import InstallMiddleware, ErrorsMiddleware
import os

app = FastAPI()

app_dir = os.path.dirname(__file__)
static_dir = os.path.join(app_dir, "app", "static")
templates_dir = os.path.join(app_dir, "app", "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

app.add_middleware(ErrorsMiddleware)
app.add_middleware(InstallMiddleware)

from app.api.routers.install import router as install_router


app.include_router(install_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9999) 
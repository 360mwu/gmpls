from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import os

app = FastAPI()


app_dir = os.path.dirname(__file__)
static_dir = os.path.join(app_dir, "app", "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=os.path.join(app_dir, "app", "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("install.html", {"request": request})

@app.get("/host-info")
async def get_host_info(request: Request):
    host = request.headers.get("host")  
    client_host = request.client.host  
    full_url = str(request.url)  

    return {
        "host": host,
        "client_host": client_host,
        "full_url": full_url,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9999)

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from app.database.database import Database
from app.models.local import DatabaseData, LocalConfig
from data.cs2_src.steamid import is_valid_profile, get_steam_id_64
from data.utils.logger import info_logger, error_logger
import json
import os

router = APIRouter()

app_dir = os.path.dirname(__file__)
templates_dir = os.path.join(app_dir, "../../templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/install", response_class=HTMLResponse)
async def install_page(request: Request):
    return templates.TemplateResponse("install.html", {"request": request})

@router.post("/check_db_connection")
async def check_db_connection(data: DatabaseData): 
    database = Database(
        host=data.db_host,
        user=data.db_user,
        password=data.db_password,
        db=data.db_name,
        port=data.db_port,
        prefix=data.db_prefix  
    )
    
    is_connected = await database.check_connection()
    
    if not is_connected:
        raise HTTPException(status_code=400, detail="Не удалось подключиться к базе данных!")
    
    return {"connected": True}

@router.post("/go_install")
async def go_install(data: LocalConfig):
    if not await is_valid_profile(data.steam_64_general_admin):
        await error_logger("Invalid Steam URL!")
        raise HTTPException(status_code=400, detail="Невалидный Steam URL")

    local_config = {
        "steam_api_key": data.steam_api_key,
        "steam_64_general_admin": data.steam_64_general_admin,
        "db_host": data.db_host,
        "db_user": data.db_user,
        "db_password": data.db_password,
        "db_name": data.db_name,
        "db_port": data.db_port,
        "db_prefix": data.db_prefix
    }

    try:
        with open('app/database/local.json', 'w') as f:
            json.dump(local_config, f, indent=4)
    except IOError as e:
        await error_logger(f"Error save config as: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении конфигурации")

    await info_logger("Success install!")
    return {"message": "Установка прошла успешно!"}


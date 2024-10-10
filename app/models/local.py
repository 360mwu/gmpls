from pydantic import BaseModel

class DatabaseData(BaseModel):
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int  
    db_prefix: str

class LocalConfig(BaseModel):
    steam_api_key: str
    steam_64_general_admin: str
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int  
    db_prefix: str

class LocalConfigCheck(BaseModel):
    steam_api_key: str
    steam_64_general_admin: int
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int  
    db_prefix: str
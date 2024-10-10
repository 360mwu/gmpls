from loguru import logger

logger.remove()

logger.add("logs/info.log", format="[{time:DD-MM-YYYY hh:mm}] [{level}] -> {message}", level="INFO", rotation="1 day", compression="zip", filter=lambda record: record["level"].name == "INFO")
logger.add("logs/error.log", format="[{time:DD-MM-YYYY hh:mm}] [{level}] -> {message}", level="ERROR", rotation="1 day", compression="zip", filter=lambda record: record["level"].name == "ERROR")

async def info_logger(message: str):
    logger.info(message)

async def error_logger(message: str):
    logger.error(message)
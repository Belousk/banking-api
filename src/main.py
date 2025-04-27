from fastapi import FastAPI
from src.api.v1 import api_router
import uvicorn
from src.swagger.tags_metadata import tags_metadata

app = FastAPI(
    title="TSMBank API",
    version="1.0.0",
    description="API for TSM Bank microservices project",
    openapi_tags=tags_metadata
)

# Подключение всех роутеров
app.include_router(api_router)

# Запуск через Python напрямую
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",          # Путь до приложения (ПутьМодуля:Переменная)
        host="127.0.0.1",         # Хост для запуска
        port=8000,                # Порт для сервера
        reload=True,              # Автоперезапуск при изменениях (для разработки)
    )

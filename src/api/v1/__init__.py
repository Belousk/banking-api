import importlib
import pkgutil
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

# Импортируем все роутеры из текущего пакета
package = __name__  # src.api.v1

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{package}.{module_name}")
    if hasattr(module, "router"):
        api_router.include_router(module.router)

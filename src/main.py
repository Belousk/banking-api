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

# Connecting all route(api routes)
app.include_router(api_router)

# Starting uvicorn by running main.py file
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,              # Autoreload when smth changed(for develop)
    )

# TODO make some documentation for funcs in files
from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.app_settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
def read_root():
    return {'Hello': 'World'}

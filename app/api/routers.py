from fastapi import APIRouter

from app.api.endpoints.anime import router as anime_router
from app.api.endpoints.director import router as director_router
from app.api.endpoints.genre import router as genre_router
from app.api.endpoints.studio import router as studio_router

ANIME_PREFIX = "/anime"
GENRE_PREFIX = "/genre"
DIRECTOR_PREFIX = "/director"
STUDIO_PREFIX = "/studio"

main_router = APIRouter(prefix="/api")

main_router.include_router(anime_router.router, prefix=ANIME_PREFIX, tags=["Anime"])
main_router.include_router(director_router.router, prefix=DIRECTOR_PREFIX, tags=["Director"])
main_router.include_router(genre_router.router, prefix=GENRE_PREFIX, tags=["Genre"])
main_router.include_router(studio_router.router, prefix=STUDIO_PREFIX, tags=["Studio"])

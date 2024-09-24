from fastapi import APIRouter
from api.V1.endpoists import curso, curso_images


api_router = APIRouter()
api_router.include_router(curso.router, prefix='/cursos', tags=['cursos'])
api_router.include_router(curso_images.router, prefix='/images', tags=['cursos'])
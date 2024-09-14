from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlmodel import select # type: ignore
from core.deps import get_session
from models.Curso_Model import Curso_model
from sqlmodel.sql.expression import Select, SelectOfScalar # type: ignore

SelectOfScalar.inherit_cache =  True
Select.inherit_cache = True

router = APIRouter()


#-------------------------------------------------------------
#       GET ALL
#-------------------------------------------------------------
@router.get('/', status_code=status.HTTP_202_ACCEPTED, response_model=List[Curso_model])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Curso_model)
        result =  await session.execute(query)
        cursos: List[Curso_model] = result.scalars().all()
        return cursos

#-------------------------------------------------------------
#       GET BY ID
#-------------------------------------------------------------
@router.get('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Curso_model)
async def get_curso_by_id(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
       
        query = select(Curso_model).filter(Curso_model.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
            
        if curso is not None:
            return curso
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)
            

#-------------------------------------------------------------
#       POST CADASTRO
#-------------------------------------------------------------
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Curso_model)
async def cadastra_curso(db: AsyncSession = Depends(get_session), curso:Curso_model=None):
    novo_curso = Curso_model(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas
    )
    db.add(novo_curso)
    await db.commit()
    return novo_curso

#-------------------------------------------------------------
#       PUT EDITA
#-------------------------------------------------------------
@router.put('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Curso_model)
async def edita_curso(curso_id: int, curso:Curso_model, db: AsyncSession = Depends(get_session)):
    async with db:
        query  = select(Curso_model).filter(Curso_model.id == curso_id)
        result = await db.execute(query)

        curso_update = result.scalar_one_or_none()

        if curso_update is None:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        curso_update.horas  = curso.horas
        curso_update.aulas  = curso.aulas
        curso_update.titulo = curso.titulo

        await db.commit()
        return curso_update

#-------------------------------------------------------------
#       DELETE
#-------------------------------------------------------------
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession=Depends(get_session)):
    async with db:
        query  = select(Curso_model).filter(Curso_model.id == curso_id)
        result = await db.execute(query)

        curso_delete = result.scalar_one_or_none()

        if curso_delete is None:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)

        await db.delete(curso_delete)
        await db.commit()
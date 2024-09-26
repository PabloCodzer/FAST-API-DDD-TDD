from typing import List
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlmodel import select, func, outerjoin # type: ignore


from core.deps import get_session
from models.User_Model import User_Model, Photo_Model
from sqlmodel.sql.expression import Select, SelectOfScalar # type: ignore
from core import auth

SelectOfScalar.inherit_cache =  True
Select.inherit_cache = True

router = APIRouter()

#-------------------------------------------------------------
#       GET ALL
#-------------------------------------------------------------
@router.get('/', status_code=status.HTTP_202_ACCEPTED)
async def get_users(db: AsyncSession = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):

    await auth.get_current_user(db, token)

    async with db as session:
        query = select(
                        User_Model.id, 
                        User_Model.name, 
                        User_Model.email, 
                        Photo_Model.nome
                    ).outerjoin(Photo_Model, Photo_Model.user_id == User_Model.id)
        result =  await session.execute(query)
        users = result.all()

        if len(users) > 0 :
            users_dto = []
            for user_id, user_name, user_email, photo_name in users:
                if photo_name is None: 
                    photo_name = 'N/A'
                user_dto = {
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_email": user_email,
                    "photo_name": photo_name,
                    "photo_url" : f"http://127.0.0.1:8000/api/v1/images/images/{photo_name}"
                }
                users_dto.append(user_dto)
            return users_dto
        else:
            raise HTTPException(detail="Nenhum usuário encontrado", status_code=status.HTTP_404_NOT_FOUND)

#-------------------------------------------------------------
#       GET BY ID
#-------------------------------------------------------------
@router.get('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def get_curso_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
       
        query = select(User_Model, Photo_Model).join(Photo_Model, isouter=True).where(User_Model.id == user_id)
        result = await session.execute(query)
        user = result.all()

        if len(user) > 0:
            users_dto = {}
            for usr, foto in user:
                if usr is not None:
                    users_dto['id'] = usr.id
                    users_dto['name'] = usr.name
                    users_dto['email'] = usr.email
                    users_dto['photo_name'] = 'N/A'
                    users_dto['photo_url'] = f"http://127.0.0.1:8000/api/v1/images/images/N/A"
                if foto is not None:
                    foto_nome = foto.nome if foto.nome is not None else 'N/A'
                    users_dto['photo_name'] = foto_nome
                    users_dto['photo_url'] =f"http://127.0.0.1:8000/api/v1/images/images/{foto_nome}"
            return users_dto
        else:
            raise HTTPException(detail="Usuario não encontrado", status_code=status.HTTP_404_NOT_FOUND)
      

#-------------------------------------------------------------
#       GET BY EMAIL
#-------------------------------------------------------------
@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(usuario: auth.LogIN, db: AsyncSession = Depends(get_session)):
    async with db as session:
       
        query = select(User_Model).filter(User_Model.email == usuario.email)
        result = await session.execute(query)
        users_by_email: List[User_Model] = result.scalars().all()
        
        if len(users_by_email) == 0:
            raise HTTPException(detail="Usuario não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
        if auth.verify_password( usuario.password, users_by_email[0].password) == False:
            raise HTTPException(detail="Senha incorreta", status_code=status.HTTP_404_NOT_FOUND)
        
        return auth.cria_token("token_login", timedelta(minutes=20) ,  usuario.email) 
    
#-------------------------------------------------------------
#       POST CADASTRO
#-------------------------------------------------------------
@router.post('/', status_code=status.HTTP_201_CREATED)
async def cadastra_curso(db: AsyncSession = Depends(get_session), user:User_Model=None):

    novo_user = User_Model(
        password=auth.get_password_hash(user.password),
        email=user.email,
        name=user.name
    )

    db.add(novo_user)
    await db.commit()
    
    return {
                "id": novo_user.id,
                "name": novo_user.name,
                "email": novo_user.email,
            }
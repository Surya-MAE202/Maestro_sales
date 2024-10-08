from fastapi import APIRouter
from .endpoints import login,user,masters,dropdown

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(user.router,tags=["User"],prefix="/user")
api_router.include_router(masters.router,tags=["Masters"],prefix="/masters")
api_router.include_router(dropdown.router,tags=["Dropdown"],prefix="/dropdown")
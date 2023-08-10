from fastapi import APIRouter, Request, Depends

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Server is running"}
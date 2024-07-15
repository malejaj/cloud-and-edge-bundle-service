from fastapi import APIRouter

router = APIRouter()

@router.post("/detect-cliff")
def detect_cliff(data:dict):
    
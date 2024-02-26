from fastapi import APIRouter
from model.loader import model  # 모델 로드

router = APIRouter()

@router.post("/inference")
async def do_inference():
    # 여기에 추론 로직 구현
    return {"message": "This is an inference API endpoint."}
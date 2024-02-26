from fastapi import APIRouter

router = APIRouter()

@router.post("/inference")
async def do_inference():
    # 여기에 추론 로직 구현
    return {"message": "This is an inference API endpoint."}
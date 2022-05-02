from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create_questions():
    return {"questions_num": "Hello World"}

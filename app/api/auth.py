from fastapi import APIRouter

router = APIRouter()

@router.post("/send-code")
async def send_code(phone: str):
    # Временная заглушка, чтобы проверить, что всё работает
    return {"message": f"Код для номера {phone} успешно создан"}
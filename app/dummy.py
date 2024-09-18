from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def get_users():
    return {"message": "Users route"}

app.include_router(router)

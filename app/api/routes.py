from fastapi import APIRouter


router=APIRouter(
    prefix="/load",
    tags=["Data Load"]
)

@router.get("/datas")
def get_all_data():
    pass
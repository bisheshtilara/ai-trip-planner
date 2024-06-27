from fastapi import APIRouter
from helper.path_finder.path_finder import path_finder
from pydantic import BaseModel

router = APIRouter()

class travelOptimizer(BaseModel):
    origin: str
    destination: str

@router.post("/path-finder")
def path_finder_router(data: travelOptimizer):
    try:
        result = path_finder(data.origin, data.destination)

        return {"message": "POST path finder", "data": result ,"code_status": 200}
    except Exception as e:
        return {"message": "POST path finder", "data": {}, "code_status": 404, "error": str(e)}

from fastapi import APIRouter, Depends

from auth import get_current_user
from gemini_service import generate_recommendation
from models import User
from schemas import HomeRecommendRequest, JewelryRecommendRequest, PartyRecommendRequest

router = APIRouter(prefix="/recommend", tags=["recommendations"])


@router.post("/home")
async def recommend_home(body: HomeRecommendRequest, _: User = Depends(get_current_user)):
    return await generate_recommendation("home", body.model_dump())


@router.post("/party")
async def recommend_party(body: PartyRecommendRequest, _: User = Depends(get_current_user)):
    return await generate_recommendation("party", body.model_dump())


@router.post("/jewelry")
async def recommend_jewelry(body: JewelryRecommendRequest, _: User = Depends(get_current_user)):
    return await generate_recommendation("jewelry", body.model_dump())

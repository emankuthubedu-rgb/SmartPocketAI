from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    identifier: str = Field(min_length=1)
    password: str = Field(min_length=1)


class PublicUser(BaseModel):
    name: str
    username: str
    email: EmailStr


class AuthResponse(BaseModel):
    token: str
    user: PublicUser


class SessionInfoResponse(BaseModel):
    username: str
    login_time: str
    session_duration_minutes: int


class HistoryCreate(BaseModel):
    type: Literal["home", "party", "jewelry"]
    title: str = Field(min_length=1, max_length=255)
    input: Dict[str, Any]
    result: Dict[str, Any]


class HistoryResponse(HistoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    createdAt: str


class Rooms(BaseModel):
    living: bool = False
    kitchen: bool = False
    bedroom: bool = False


class HomeRecommendRequest(BaseModel):
    totalBudget: float = Field(gt=0)
    rooms: Rooms
    lights: int = Field(ge=0)
    fans: int = Field(ge=0)
    furniture: int = Field(ge=0)
    diningTables: int = Field(ge=0)
    additional: str = ""


class PartyRecommendRequest(BaseModel):
    totalBudget: float = Field(gt=0)
    guests: int = Field(ge=1)
    eventType: str
    venueType: str
    needsCatering: bool
    needsDecoration: bool
    needsEntertainment: bool
    needsPhotography: bool
    needsGifts: bool
    additional: str = ""


class JewelryRecommendRequest(BaseModel):
    totalBudget: float = Field(gt=0)
    occasion: str
    style: str
    outfitImage: Optional[str] = None


class ShoppingLink(BaseModel):
    label: str
    url: str


class RecommendationItem(BaseModel):
    name: str
    description: str
    quantity: int = Field(ge=1)
    estimated_price: float = Field(ge=0)
    shopping_links: List[ShoppingLink]


class BudgetCategory(BaseModel):
    label: str
    icon: Literal[
        "sofa", "party", "gem", "bulb", "fan", "table", "utensils",
        "balloon", "music", "aperture", "gift", "building", "palette"
    ]
    allocation: float = Field(ge=0)
    total_cost: float = Field(ge=0)
    percentage_of_budget: float = Field(ge=0)
    items: List[RecommendationItem]


class OutfitAnalysis(BaseModel):
    colors: List[str]
    style: str
    formality: str


class VenueSuggestion(BaseModel):
    name: str
    type: str
    capacity: int
    estimated_cost: float
    shopping_links: List[ShoppingLink]


class RecommendationResponse(BaseModel):
    total_budget: float
    spent: float
    remaining_budget: float
    guests: Optional[int] = None
    occasion: Optional[str] = None
    outfit_analysis: Optional[OutfitAnalysis] = None
    outfit_image: Optional[str] = None
    budget_breakdown: List[BudgetCategory]
    venue_suggestions: Optional[List[VenueSuggestion]] = None
    additional_suggestions: List[str]

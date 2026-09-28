import asyncio
import base64
import json
import os
from typing import Any, Dict, Optional, Tuple
from urllib.parse import quote_plus
 
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError
 
from schemas import RecommendationResponse
 
load_dotenv()
 
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
TIMEOUT_SECONDS = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "45"))
ALLOWED_ICONS = [
    "sofa", "party", "gem", "bulb", "fan", "table", "utensils",
    "balloon", "music", "aperture", "gift", "building", "palette",
]
 
 
def _model():
    if not API_KEY:
        raise HTTPException(status_code=503, detail="Gemini is not configured. Set GEMINI_API_KEY.")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.25,
        },
    )
 
 
def _links(term: str, planner: str):
    q = quote_plus(term)
    if planner == "jewelry":
        return [
            {"label": "Amazon", "url": f"https://www.amazon.in/s?k={q}"},
            {"label": "Tanishq", "url": f"https://www.tanishq.co.in/search?q={q}"},
        ]
    if planner == "party":
        return [
            {"label": "Google", "url": f"https://www.google.com/search?q={q}"},
            {"label": "Amazon", "url": f"https://www.amazon.in/s?k={q}"},
        ]
    return [
        {"label": "Amazon", "url": f"https://www.amazon.in/s?k={q}"},
        {"label": "Flipkart", "url": f"https://www.flipkart.com/search?q={q}"},
    ]
 
 
def _schema_instruction(planner: str) -> str:
    extras = {
        "home": 'Do not include guests, occasion, outfit_analysis, outfit_image or venue_suggestions.',
        "party": 'Include guests and venue_suggestions. Do not include occasion, outfit_analysis or outfit_image.',
        "jewelry": 'Include occasion, outfit_analysis and outfit_image. Do not include guests or venue_suggestions.',
    }[planner]
    more = {"home": "", "party": ", guests, venue_suggestions", "jewelry": ", occasion, outfit_analysis, outfit_image"}[planner]
    return f"""
Return ONLY one valid JSON object. No markdown and no commentary.
The top-level JSON keys must be named exactly: budget_breakdown (array of categories), additional_suggestions (array of strings){more}.
Example shape: {{"budget_breakdown": [{{"label": "Lighting", "icon": "bulb", "allocation": 3000, "total_cost": 2800, "percentage_of_budget": 18.2, "items": [{{"name": "LED bulb pack", "description": "Pack of 10 9W bulbs", "quantity": 1, "estimated_price": 800, "shopping_links": [{{"label": "Amazon", "url": "https://www.amazon.in/s?k=LED+bulb+pack"}}]}}]}}], "additional_suggestions": ["..."]}}
budget_breakdown must contain at least 2 categories, each with at least 1 item.
Use INR amounts as numbers, not strings. Never exceed the supplied total budget.
Each category must contain label, icon, allocation, total_cost, percentage_of_budget and items.
Each item must contain name, description, quantity, estimated_price and shopping_links.
Use only these icon keys: {', '.join(ALLOWED_ICONS)}.
shopping_links must be an array of objects with label and url. Use real search URLs, not invented product pages.
additional_suggestions must be an array of strings.
{extras}
"""
 
 
def _build_prompt(planner: str, payload: dict, has_image: bool) -> str:
    return f"""You are Smartpocket AI, a practical Indian budget allocation assistant.
Create a useful {planner} plan from the user's data. Prefer realistic categories and quantities.
Calculate totals carefully. allocation is the category allowance; total_cost is the sum of its item estimated_price values.
percentage_of_budget is total_cost / totalBudget * 100.
For jewelry with an image, analyze visible outfit colors, style and formality and return outfit_analysis.
User input: {json.dumps(payload, ensure_ascii=False)}
Image supplied: {has_image}
{_schema_instruction(planner)}"""
 
 
def _decode_data_url(data_url: str) -> Tuple[str, bytes]:
    try:
        header, encoded = data_url.split(",", 1)
        mime = header.split(";")[0].split(":", 1)[1]
        if not mime.startswith("image/"):
            raise ValueError("Unsupported media type")
        return mime, base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="outfitImage must be a valid base64 image data URL.") from exc
 
 
def _normalize(raw: Dict[str, Any], planner: str, payload: dict, outfit_image: Optional[str]):
    budget = round(float(payload["totalBudget"]), 2)
    raw["total_budget"] = budget
 
    if planner == "party":
        raw["guests"] = int(payload["guests"])
        raw.setdefault("venue_suggestions", [])
    elif planner == "jewelry":
        raw["occasion"] = payload["occasion"]
        raw["outfit_image"] = outfit_image
        if not outfit_image:
            raw["outfit_analysis"] = None
 
    if not raw.get("budget_breakdown"):
        for alt in ("breakdown", "categories", "budget_categories", "budget"):
            if isinstance(raw.get(alt), list) and raw[alt]:
                raw["budget_breakdown"] = raw.pop(alt)
                break
 
    breakdown = raw.get("budget_breakdown") or []
    if not breakdown:
        raise HTTPException(status_code=502, detail="Gemini returned no budget categories. Please try again.")
 
    for category in breakdown:
        if category.get("icon") not in ALLOWED_ICONS:
            category["icon"] = {"home": "sofa", "party": "party", "jewelry": "gem"}[planner]
        items = category.get("items") or []
        for item in items:
            item["quantity"] = max(1, int(item.get("quantity") or 1))
            item["estimated_price"] = max(0.0, float(item.get("estimated_price") or 0))
            if not item.get("shopping_links"):
                item["shopping_links"] = _links(str(item.get("name", "recommendation")), planner)
        category["items"] = items
        category["total_cost"] = round(sum(i["estimated_price"] for i in items), 2)
 
    original_spent = sum(float(c.get("total_cost") or 0) for c in breakdown)
    if original_spent > budget and original_spent > 0:
        scale = budget / original_spent
        for category in breakdown:
            for item in category["items"]:
                item["estimated_price"] = round(item["estimated_price"] * scale, 2)
            category["total_cost"] = round(sum(i["estimated_price"] for i in category["items"]), 2)
            category["allocation"] = min(
                round(float(category.get("allocation") or category["total_cost"]) * scale, 2),
                category["total_cost"],
            )
 
    spent = round(sum(float(c.get("total_cost") or 0) for c in breakdown), 2)
    if spent > budget:  # absorb floating-point rounding in the last priced item
        excess = round(spent - budget, 2)
        for category in reversed(breakdown):
            if category["items"]:
                last = category["items"][-1]
                last["estimated_price"] = round(max(0, last["estimated_price"] - excess), 2)
                category["total_cost"] = round(sum(i["estimated_price"] for i in category["items"]), 2)
                break
        spent = round(sum(c["total_cost"] for c in breakdown), 2)
 
    for category in breakdown:
        category["allocation"] = round(max(category["total_cost"], float(category.get("allocation") or 0)), 2)
        category["percentage_of_budget"] = round((category["total_cost"] / budget) * 100, 2) if budget else 0
 
    raw["budget_breakdown"] = breakdown
    raw["spent"] = min(spent, budget)
    raw["remaining_budget"] = round(max(0, budget - raw["spent"]), 2)
    raw.setdefault("additional_suggestions", [])
 
    allowed = {
        "total_budget", "spent", "remaining_budget", "budget_breakdown",
        "additional_suggestions", "guests", "occasion", "outfit_analysis",
        "outfit_image", "venue_suggestions",
    }
    cleaned = {key: value for key, value in raw.items() if key in allowed}
    try:
        return RecommendationResponse.model_validate(cleaned).model_dump(exclude_none=False)
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail=f"Gemini returned an unusable recommendation structure: {exc.errors()[0]['msg']}") from exc
 
 
async def generate_recommendation(planner: str, payload: dict) -> dict:
    outfit_image = payload.get("outfitImage") if planner == "jewelry" else None
    prompt_payload = {k: v for k, v in payload.items() if k != "outfitImage"}
    parts: list[Any] = [_build_prompt(planner, prompt_payload, bool(outfit_image))]
    if outfit_image:
        mime, image_bytes = _decode_data_url(outfit_image)
        parts.append({"mime_type": mime, "data": image_bytes})
 
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(_model().generate_content, parts),
            timeout=TIMEOUT_SECONDS,
        )
        text = response.text
        print("=== GEMINI RAW RESPONSE ===")
        print(text)
        print("=== END GEMINI RAW RESPONSE ===")
        data = json.loads(text)
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=502, detail="Gemini request timed out. Please try again.") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="Gemini returned invalid JSON. Please try again.") from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini API request failed: {str(exc)}") from exc
 
    return _normalize(data, planner, payload, outfit_image)
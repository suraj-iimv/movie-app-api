from fastapi import APIRouter, HTTPException
from api.schemas import ApiResponse, MovieSearchRequest, MovieSearchResponse, SuggestionsResponse
from services.ai_service import AIService

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/api/search", response_model=ApiResponse[MovieSearchResponse])
async def search_movie(request: MovieSearchRequest):
    try:
        movie_data = await AIService.search_movie(request.query)
        if "error" in movie_data:
            return ApiResponse(success=False, error=movie_data["error"])
        
        return ApiResponse(
            success=True,
            data=MovieSearchResponse(**movie_data)
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))

@router.get("/api/suggestions", response_model=ApiResponse[SuggestionsResponse])
async def get_suggestions(q: str):
    try:
        suggestions = await AIService.get_suggestions(q)
        return ApiResponse(
            success=True,
            data=SuggestionsResponse(suggestions=suggestions)
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))

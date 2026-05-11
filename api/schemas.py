from pydantic import BaseModel
from typing import List, Optional, Any, Generic, TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

class MovieSearchRequest(BaseModel):
    query: str

class MovieSearchResponse(BaseModel):
    title: str
    release_year: str
    director: str
    cast: List[str]
    ratings: str
    plot: str
    similar_movies: List[str]

class SuggestionsResponse(BaseModel):
    suggestions: List[str]

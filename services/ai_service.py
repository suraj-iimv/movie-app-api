import httpx
import json
from typing import List, Optional
from config.settings import settings

class AIService:
    @staticmethod
    async def search_movie(query: str) -> dict:
        system_prompt = """You are a movie database API. Respond ONLY with a valid JSON object. No markdown formatting, no code blocks, no additional text. 
The user will provide a movie name. Find the most relevant popular movie and return the following JSON structure:
{
    "title": "Exact Movie Title",
    "release_year": "YYYY",
    "director": "Director Name",
    "cast": ["Actor 1", "Actor 2", "Actor 3", "Actor 4", "Actor 5"],
    "ratings": "e.g., 8.8/10 IMDb",
    "plot": "A short, engaging 2-3 sentence plot summary.",
    "similar_movies": ["Movie 1", "Movie 2", "Movie 3"]
}
If the movie cannot be found, return a JSON object with an "error" key: {"error": "Movie not found"}."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Movie AI Proxy"
                },
                json={
                    "model": "openai/gpt-oss-120b:free",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f'Find information for the movie: "{query}"'}
                    ],
                    "temperature": 0.2
                },
                timeout=30.0
            )
            
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content'].strip()
            
            # Clean potential markdown formatting
            if content.startswith('```json'):
                content = content.replace('```json', '', 1).rsplit('```', 1)[0].strip()
            elif content.startswith('```'):
                content = content.replace('```', '', 1).rsplit('```', 1)[0].strip()
                
            return json.loads(content)

    @staticmethod
    async def get_suggestions(query: str) -> List[str]:
        if not query or len(query) < 2:
            return []

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-120b:free",
                    "messages": [
                        {"role": "system", "content": "You are a movie suggestion engine. Return ONLY a comma-separated list of the 5 most popular movie titles that match the user query. No other text."},
                        {"role": "user", "content": query}
                    ],
                    "max_tokens": 50,
                    "temperature": 0
                },
                timeout=15.0
            )
            
            response.raise_for_status()
            data = response.json()
            text = data['choices'][0]['message']['content'].strip()
            return [s.strip() for s in text.split(',') if s.strip()]

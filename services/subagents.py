from services.polymarket_service import get_order_book
from services.weather_service import get_weather
from services.llm_service import generate_response

def research_subagent(prompt: str, language="en"):
    return generate_response(prompt, language=language)

def weather_subagent(city: str):
    return get_weather(city)

def orderbook_subagent(market_id: str):
    return get_order_book(market_id)
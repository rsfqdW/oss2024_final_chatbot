import asyncio
from chatbot import Chat, register_call
import os
import wikipedia
import python_weather
import datetime


import warnings
warnings.filterwarnings("ignore")

@register_call("do_you_know")
def do_you_know(session=None, query=None):
    return "I do not know about " + query

@register_call("weather")
def call_weather(session=None, city='New York'):
    global weather_string
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(get_weather(city))
    except Exception:
        weather_string = "I don't know the weather."
    
    print(f"{city}의 날씨 정보:")
    print(weather_string)
    return weather_string

weather_string = None

##weather_string 수정
async def get_weather(city='New York'):
    global weather_string
    async with python_weather.Client() as client:
        weather = await client.get(city)
        await client.close()
    
    today = datetime.date.today()
    weather_string = f"{city}의 {today.strftime('%Y년 %m월 %d일')} 날씨 예보:\n"
    weather_string += "="*40 + "\n"
    weather_string += "시간  | 온도 | 날씨\n"
    weather_string += "-"*40 + "\n"
    for hourly in list(weather.daily_forecasts)[0].hourly_forecasts:
        weather_string += f"{hourly.time.strftime('%H:%M')} | {hourly.temperature:>3}°C | {hourly.description:<15}\n"
    weather_string += "="*40

@register_call("wiki")
def who_is(session=None, query='South Korea'):
    try:
        return wikipedia.summary(query)
    except Exception:
        pass
    return "I don't know about "+query


first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_test.template"))
chat.converse(first_question)
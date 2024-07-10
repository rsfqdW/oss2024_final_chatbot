import asyncio
from chatbot import Chat, register_call
import os
import wikipedia
import python_weather


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
        asyncio.run(get_weather())
    except Exception:
        weather_string = "I do not know the weather"
    return weather_string

weather_string = None

async def get_weather(city='New York'):
    global weather_string
    async with python_weather.Client() as client:
        weather = await client.get(city)
        await client.close()
    weather_string = ""
    for hourly in list(weather.daily_forecasts)[0].hourly_forecasts:
        weather_string = weather_string + str(hourly.time) + " " + str(hourly.temperature) + " deg.C " + str(hourly.description) + "\n"

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
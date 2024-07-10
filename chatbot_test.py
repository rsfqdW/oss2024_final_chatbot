import asyncio
from chatbot import Chat, register_call
import os
import wikipedia
import python_weather
from horoscope_data import horoscopes
import datetime
from food_data import KoreanCuisine,ChineseCuisine,WesternCuisine,JapaneseCuisine,ItalianCuisine
import requests
from datetime import datetime, timedelta
import random  # random 모듈 추가
from horoscope_data import horoscopes  # 추가된 부분

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
    
@register_call("horoscope")
def get_horoscope(session=None, sign = 'leo'):
    try:
        return random.choice(horoscopes)
    except Exception:
        return "I don't know the general horoscope for today"
       
@register_call("food")
def get_food(session=None, sign = "Korean food"):
    try:
        random_number = random.randint(1,5)
        if random_number == 1:
            return random.choice(KoreanCuisine)
        elif random_number == 2:
            return random.choice(ChineseCuisine)
        elif random_number == 3:
            return random.choice(WesternCuisine)
        elif random_number == 4:
            return random.choice(JapaneseCuisine)
        elif random_number == 5:
            return random.choice(ItalianCuisine)
    except Exception:
        return sign

@register_call("box_office")
def call_box_office(session=None, query=None):
    api_key = "a734e5765f4da2c8539af53bbc793e5d"  # API 키
    target_date = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
    url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={target_date}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        box_office_result = "box office ranking:\n"
        for item in data['boxOfficeResult']['dailyBoxOfficeList']:
            box_office_result += f"{item['rank']}. {item['movieNm']}\n"
        return box_office_result
    else:
        return "Failed to retrieve box office data"

first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_test.template"))
chat.converse(first_question)
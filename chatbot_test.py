import asyncio
import random  # random 모듈 추가
from chatbot import Chat, register_call
import os
import requests
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
    

horoscopes = [
    "오늘 당신의 운세는 밝은 태양처럼 빛날 것입니다. 모든 일에 긍정적인 에너지를 가지고 임하세요. 예상치 못한 행운이 다가올 수 있습니다.",
    "오늘은 평소보다 더 큰 결단력이 필요할 수 있습니다. 자신을 믿고, 중요한 결정을 내릴 때 주저하지 마세요.",
    "오늘은 다른 사람과의 협력이 중요한 날입니다. 팀워크를 통해 더 큰 성과를 얻을 수 있을 것입니다.",
    "오늘은 약간의 도전이 기다리고 있을 수 있지만, 그것을 이겨내면 큰 성장을 이룰 수 있을 것입니다. 끈기와 인내가 필요합니다.",
    "오늘은 사랑과 애정이 넘치는 하루가 될 것입니다. 가족이나 친구와 함께 소중한 시간을 보내세요.",
    "오늘은 직장에서의 노력이 인정받는 날이 될 것입니다. 꾸준히 열심히 해온 일들이 빛을 발할 때입니다.",
    "오늘은 재정적으로 좋은 소식이 있을 수 있습니다. 하지만 충동적인 소비는 피하고, 현명한 선택을 하세요.",
    "오늘은 건강에 유의해야 할 날입니다. 평소보다 더 신경 써서 몸을 돌보고, 충분한 휴식을 취하세요.",
    "오늘은 창의력이 폭발하는 날입니다. 새로운 아이디어나 프로젝트에 도전해보세요. 놀라운 성과를 이룰 수 있습니다.",
    "오늘은 평소보다 더 많은 행운이 따를 것입니다. 어떤 일이든지 자신감을 가지고 시도해보세요.",
    "오늘은 과거의 실수나 후회를 떨쳐버리고 새 출발을 할 수 있는 기회입니다. 긍정적인 마인드로 하루를 시작하세요.",
    "오늘은 사람들과의 커뮤니케이션이 중요한 날입니다. 명확하고 정직하게 소통하면 좋은 결과를 얻을 수 있습니다.",
    "오늘은 당신의 재능을 인정받을 수 있는 날입니다. 자신을 표현하고, 숨기지 말고 보여주세요.",
    "오늘은 작은 변화가 큰 행복을 가져다줄 수 있습니다. 일상 속에서 새로운 시도를 해보세요.",
    "오늘은 용서와 화해의 날입니다. 오래된 갈등을 해결하고, 마음의 짐을 내려놓으세요.",
    "오늘은 자연과 함께하는 시간을 가져보세요. 산책이나 야외 활동을 통해 스트레스를 해소하고, 마음의 평화를 찾으세요.",
    "오늘은 당신의 목표를 재평가하고, 앞으로 나아갈 방향을 정할 수 있는 날입니다. 명확한 계획을 세워보세요.",
    "오늘은 직감이 당신을 이끌어 줄 것입니다. 중요한 결정을 할 때는 자신의 직감을 믿고 따르세요.",
    "오늘은 인내심이 필요한 하루입니다. 급하게 서두르지 말고, 차분하게 상황을 지켜보세요.",
    "오늘은 새로운 인연을 만날 수 있는 날입니다. 열린 마음으로 사람들을 대하고, 새로운 관계를 맺어보세요.",
    "오늘은 과감한 도전이 필요한 날입니다. 새로운 기회를 두려워하지 말고, 용기 있게 도전해보세요.",
    "오늘은 다른 사람들에게 도움을 주는 날입니다. 작은 친절이 큰 행복을 가져다줄 수 있습니다.",
    "오늘은 자신을 돌아보는 시간을 가지세요. 내면의 목소리에 귀 기울이고, 진정으로 원하는 것이 무엇인지 생각해보세요.",
    "오늘은 감사의 마음을 가지세요. 작은 일에도 감사하며, 긍정적인 에너지를 주변에 전파하세요.",
    "오늘은 새로운 취미나 활동을 시작해보세요. 일상에 변화를 주고, 새로운 즐거움을 찾을 수 있을 것입니다.",
    "오늘은 스트레스를 관리하는 날입니다. 명상이나 요가를 통해 마음의 안정을 찾고, 평온한 하루를 보내세요.",
    "오늘은 자신에게 집중하는 날입니다. 자신의 필요와 욕구를 충족시키고, 충분한 휴식을 취하세요.",
    "오늘은 가족과의 시간이 중요한 날입니다. 가까운 사람들과의 유대감을 강화하고, 따뜻한 시간을 보내세요.",
    "오늘은 당신의 꿈을 구체화하는 날입니다. 목표를 설정하고, 그 목표를 향해 한 걸음 더 나아가세요.",
    "오늘은 긍정적인 변화를 만들어가는 날입니다. 작은 변화가 큰 행복으로 이어질 수 있습니다. 긍정적인 마음으로 하루를 보내세요."
]


@register_call("horoscope")
def get_horoscope(session=None, sign = 'leo'):
    try:
        return random.choice(horoscopes)
    except Exception:
        return "I don't know the general horoscope for today"

first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_test.template"))
chat.converse(first_question)
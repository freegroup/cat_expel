import telegram
from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)

bot = telegram.Bot(token=conf.get(section="telegram", key='api_token'))
chat_id = conf.get_int(section="telegram", key="channel_id")

bot.send_video(chat_id=chat_id, video=open('test.mp4', 'rb'), supports_streaming=True, timeout=10000)


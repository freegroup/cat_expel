import slack
import time

from datetime import datetime, date

from file.configuration import Configuration

conf = Configuration(inifile="config/service.ini", reload_on_change=True)


if __name__ == "__main__":
    client = slack.WebClient(token=conf.get("api_token", section="slack"))

    now = date.today()
    channel_id = None
    res = client.channels_list(count=1000)
    for channel in res['channels']:
        if channel['name'] == conf.get("channel", section="slack"):
            channel_id = channel['id']
            break

    res = client.channels_history( channel=channel_id, count=1000)
    for message in res['messages']:
        ts = message["ts"]
        timestamp = int(float(ts))
        dt_object = date.fromtimestamp(timestamp)
        diff = now - dt_object
        if diff.days > 10:
            del_res = client.chat_delete(channel=channel_id, ts=ts)
            print(del_res)


    res = client.files_list( channels="#"+conf.get("channel", section="slack"), count=1000)
    for message in res['files']:
        timestamp = message["created"]
        dt_object = date.fromtimestamp(timestamp)
        diff = now - dt_object
        if diff.days > 10:
            del_res = client.files_delete(file=message["id"])
            print(del_res)


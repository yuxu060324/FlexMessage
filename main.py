import google.auth
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
import json
from JsonControl import JsonManager
from GoogleSchedule import get_calendar_event
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import dateutil.parser

SCOPES = ['https://www.googleapis.com/auth/calendar']

# with open('Key\\line_bot_info.json') as f:
#   line_bot_info = json.load(f)
# LINEBOT_ACCESS_TOKEN = line_bot_info['CHANNEL_ACCESS_TOKEN']
# USER_ID = line_bot_info['USER_ID']
# line_bot_api = LineBotApi(LINEBOT_ACCESS_TOKEN)


def get_calender():

  dic_proceess = {}

  return dic_proceess

def main():

  events = get_calendar_event()
  print(events)

  # JM = JsonManager()
  # JM.edit_json(LOAD_FILE_PATH, events)
  #
  # payload = JM.load_json_template_message(LOAD_FILE_PATH)
  # container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
  # line_bot_api.push_message(USER_ID, messages=container_obj)


if __name__ == "__main__":
  main()


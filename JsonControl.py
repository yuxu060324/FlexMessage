import os, re, datetime
import json
from json_global import HEADER_FILE_PATH, FOOTER_FILE_PATH, ICON_EVENT_FILE, ICON_WEATHER_FOLDER_PATH
from json_global import DAY_OF_WEEK_LIST, ICON_EVENT_FILE, ICON_WEATHER_FILE

# boxで囲むだけの関数
def pack_vertical(arr):
    return {"type": "box", "layout": "vertical", "content": arr}
def pack_horizontal(arr):
    return {"type": "box", "layout": "horizontal", "content": arr}

def pack_text(str, url=None):
    if url == None:
        return {"type": "text", "text": str}
    else:
        return {"type": "text", "text": str, "action": {"type": "url", "label": "action", "url": url}}

class JsonManager():

    def __init__(self, logger):

        self.massage_json_path = os.path.abspath(".\\FlexMessageDictionary")
        self.logger = logger

        # for message
        self._message = ""
        self._header = ""
        self._event = ""
        self._schedule = ""
        self._body = ""
        self._footer = ""

    def load_json(self, path):

        load_path = os.path.join(self.massage_json_path, path)

        if os.path.isfile(path):
            print("This file_path does not exist")
            return

        with open(load_path) as f:
            payload = json.load(f)

        return payload

    def edit_json(self, path, calendar_events):
        calendar_events = [('2023-03-09', '2023-03-10', 'テスト用'),
         ('2023-03-09T09:30:00+09:00', '2023-03-09T13:00:00+09:00', '人形町ブランドテスト AMEX'),
         ('2023-03-10T09:30:00+09:00', '2023-03-10T13:00:00+09:00', '人形町ブランドテスト Master'), ('2023-03-14T09:30:00+09:00', '2023-03-14T13:00:00+09:00', '人形町ブランドテスト VISA')]

        edit_json_data = self.load_json("schedule_base.json")

        contents = self.test_contents()
        # self.make_body_contents(type="text", texts=calendar_events)
        # self.test_contents()
        self.logger.debug(contents)

        edit_json_data['body']['contents'] = contents

        edit_path = os.path.join(self.massage_json_path, path)

        with open(edit_path, 'w') as f:
            d = json.dumps(edit_json_data, indent=2)
            f.write(d)
            self.logger.debug("finished write json")

    def make_body_contents(self, calendar_events):

        name = []
        time = []
        date = []

        if calendar_events is not None:

            for events in calendar_events:
                if re.match(r'^\d{4}-\d{2}-\d{2}$', events[0]):
                    time.append("ALL")
                    date.append('{0:%m月%d日}'.format(datetime.datetime.strptime(events[0], '%Y-%m-%d')))
                else:
                    time.append('{0:%H:%M} ~ {1:%H:%M}'.format(
                        datetime.datetime.strptime(events[0], '%Y-%m-%dT%H:%M:%S+09:00'),
                        datetime.datetime.strptime(events[1], '%Y-%m-%dT%H:%M:%S+09:00')))
                    date.append('{0:%m月%d日}'.format(
                        datetime.datetime.strptime(events[0], '%Y-%m-%dT%H:%M:%S+09:00')))
                name.append(events[2])

            contents = [
                {
                    "date": date[i],
                    "schedule": [
                        {
                            "time": time[i],
                            "name": name[i]
                        }
                    ]
                } for i in range(len(calendar_events))]

        else:
            contents = []

        # contents = [
        #     {
        #         "type": "box",
        #         "layout": "horizontal",
        #         "contents": self.make_one_schedule_contents(type="text", schedule=text)
        #     } for text in texts]

        return contents

    def test_contents(self):

        contents = [
            {
                "type": "text",
                "text": "03\u670809\u65e5",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "All Day",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": "For Test",
                                "size": "sm"
                            }
                        ]
                    }
                ]
            }
        ]

        return contents

    def make_one_schedule_contents(self, type, schedule):

        if re.match(r'^\d{4}-\d{2}-\d{2}$', schedule[0]):

            start_date = '{0:%m月%d日}'.format(datetime.datetime.strptime(schedule[1], '%Y-%m-%d'))

            contents = [
                {
                    "type": type,
                    "text": '{0} All Day'.format(start_date),
                    "size": "sm"
                },
                {
                    "type": type,
                    "text": schedule[2],
                    "size": "sm"
                }
            ]

        else:

            start_time = '{0:%m月%d日 %H:%M}'.format(
                datetime.datetime.strptime(schedule[0], '%Y-%m-%dT%H:%M:%S+09:00'))
            end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(schedule[1], '%Y-%m-%dT%H:%M:%S+09:00'))

            contents = [
                {
                    "type": type,
                    "text": '{0} ~ {1}'.format(start_time, end_time),
                    "size": "sm"
                },
                {
                    "type": type,
                    "text": schedule[2],
                    "size": "sm"
                }
            ]

        return contents

    def get_setting_filepath(self):
        return self.massage_json_path

    # Flex MessageのHeader部のパッケージ
    def package_header(self, weather="sunny"):

        # 日付の文字列
        date_today = datetime.datetime.now()
        date_wod = DAY_OF_WEEK_LIST[date_today.weekday()]
        date_str = date_today.strftime("%m 月 %d 日 ( " + date_wod + " )")

        # 天気アイコンのファイルパス
        weather_file_path = os.path.join(ICON_WEATHER_FOLDER_PATH, ICON_WEATHER_FILE[weather])

        self._header = self.load_json("temp//header.json")
        # 日付の設定
        self._header['header']['contents'][0]['contents'][1]['text'] = date_str
        # 天気アイコンの設定
        self._header['header']['contents'][1]['contents'][0]['url'] = weather_file_path

        print(self._header)

    def package_event(self):

        return 0

    def package_schedule(self):

        return 0

    # Flex MessageのBody部のパッケージ
    def package_body(self, schedule_list):

        self.package_event()
        self.package_schedule()

        if (self._event == "") and (self._schedule == ""):
            pack_text("予定なし")
        elif (self._event == ""):
            pack_vertical(self._schedule)
        elif (self._schedule == ""):
            pack_vertical(self._event)
        else:
            print("Error\n")

        return 0

    # Flex MessageのFooter部のパッケージ
    def package_footer(self):

        if os.path.isfile(FOOTER_FILE_PATH):
            self._footer = self.load_json(FOOTER_FILE_PATH)

    #     ファイルが存在しなかったらログを残す

    # Flex Messageのパッケージ
    def package_message(self):

        # Bodyがない場合はエラー
        if (self._body == ""):
            return -1

        # HeaderとFooterが無い場合はパッケージを行う
        if (self._header == ""):
            self.package_header()
        if (self._footer == ""):
            self.package_footer()

        self._message = {
            "type": "bubble",
            "size": "mega",
            "header": self._header,
            "body": self._body,
            "footer": self._footer
        }

        print(self._message)

        return self._message

    def package_message_none(self):

        self._message = self.load_json(path="sample_simple.json")

        return self._message

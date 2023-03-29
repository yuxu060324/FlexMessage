import os, re, datetime
import json

class JsonManager():

    def __init__(self):

        self.path = os.path.abspath(".\\FlexMessageDictionary")

    def load_json_template_message(self, path):

        load_path = os.path.join(self.path, path)

        with open(load_path) as f:
            payload = json.load(f)

        return payload

    def edit_json(self, path, calendar_events):
        calendar_events = [('2023-03-09', '2023-03-10', 'テスト用'),
         ('2023-03-09T09:30:00+09:00', '2023-03-09T13:00:00+09:00', '人形町ブランドテスト AMEX'),
         ('2023-03-10T09:30:00+09:00', '2023-03-10T13:00:00+09:00', '人形町ブランドテスト Master'), ('2023-03-14T09:30:00+09:00', '2023-03-14T13:00:00+09:00', '人形町ブランドテスト VISA')]

        edit_json_data = self.load_json_template_message("schedule_base.json")

        contents = self.test_contents()
        # self.make_body_contents(type="text", texts=calendar_events)
        # self.test_contents()
        print(contents)

        edit_json_data['body']['contents'] = contents

        edit_path = os.path.join(self.path, path)

        with open(edit_path, 'w') as f:
            d = json.dumps(edit_json_data, indent=2)
            f.write(d)

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
        return self.path

events = [
    {
        "date": "03-09",
        "schedule": [
            {
                "time": "All",
                "name": "For Test"
            },
            {
                "time": "9:30 ~ 13:00",
                "name": "Brand Test"
            }
        ]
    },
    {
        "date": "03-10",
        "schedule": [
            {
                "time": "9:30 ~ 13:00",
                "name": "Brand Test"
            }
        ]
    }
]

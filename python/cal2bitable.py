import sys
import re
import json
import caldav
from datetime import date
from datetime import datetime
from datetime import timedelta
from flask import Flask, jsonify, make_response, request

def getCaldavInfo():
    data = request.get_json()
    if data is None or data == "":
        return {}
    paramsStr = data.get("params")
    if paramsStr is None or paramsStr == "":
        return {}
    params = json.loads(paramsStr)
    datasourceConfigStr = params.get("datasourceConfig")
    if datasourceConfigStr is None:
        return {}
    return json.loads(datasourceConfigStr)

def checkCaldavInfo(caldavInfo) :
    if caldavInfo is None:
        return False
    print("caldavInfo", caldavInfo.get("caldavURL"), caldavInfo.get("caldavUser"))
    if caldavInfo.get("caldavURL") is None or caldavInfo.get("caldavURL") == "":
        return False
    if caldavInfo.get("caldavUser") is None or caldavInfo.get("caldavUser") == "":
        return False
    if caldavInfo.get("caldavPass") is None or caldavInfo.get("caldavPass") == "":
        return False
    return True

def syncEvents():
    caldavInfo = getCaldavInfo()
    if checkCaldavInfo(caldavInfo) == False:
        return []
    with caldav.DAVClient(
        url=caldavInfo.get("caldavURL"),
        username=caldavInfo.get("caldavUser"),
        password=caldavInfo.get("caldavPass"),
    ) as client:
        my_principal = client.principal()
        calendars = my_principal.calendars()

    print("your principal has %i calendars:" % len(calendars))
    calendars = sorted(calendars, key=lambda c: c.name)
    ret = []
    for c in calendars:
        print("    Name: %-36s  URL: %s" % (c.name, c.url))
        events = c.objects_by_sync_token("", load_objects=False)
        events = c.calendar_multiget([event.url for event in events])
        events = [event for event in events if event.vobject_instance is not None]
        events = sorted(events, key=lambda event: event.vobject_instance.vevent.dtstart.value)
        for event in events:
            description = re.sub(r"视频会议:\shttps://vc.feishu.cn/j/\d+\n", "", event.instance.vevent.description.value)
            ret.append(
                {
                    "primaryId": event.instance.vevent.uid.value,
                    "data": {
                        "fid_title": event.instance.vevent.summary.value,
                        "fid_start_time": event.instance.vevent.dtstart.value.timestamp()*1000,
                        "fid_end_time": event.instance.vevent.dtend.value.timestamp()*1000,
                        "fid_duration_minutes": (event.instance.vevent.dtend.value.timestamp() - event.instance.vevent.dtstart.value.timestamp()) / 60,
                        "fid_description": description,
                        "fid_calender_name": c.name,
                    }
                }
            )
    return ret
        


app = Flask(__name__)

@app.route('/cal2bitable/api/')
def hello_world():
    return 'Hello, World!'

@app.route('/cal2bitable/api/records', methods=['GET', 'POST'])
def records():
    events = syncEvents()
    res = {
        "code": 0,
        "msg": "",
        "data": {
            "nextPageToken": "",
            "hasMore": False,
            "records": events
        }
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run()
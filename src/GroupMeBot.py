import time
import requests
from src import spreadsheet

# url for the group "Test Group"
url = 'https://api.groupme.com/v3/groups/44100309/messages'
request_parameters = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO'}
# The 20 most recent messages, https://dev.groupme.com/docs/v3#messages
resp_msgs = requests.get(url, params=request_parameters).json()['response']['messages']


new_prams = {
    'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO',
    'after_id': resp_msgs[19]["id"]
}

# reload the name conversion sheet once before entering loop
spreadsheet.reload_name_conversion()
while 1:
    response = requests.get(url, params=new_prams)
    new_msgs = response.json()['response']['messages']
    # gets the most recent events, after the id of the last event called.

    for message in new_msgs:
        if "LogisticsBot sheet" in message["text"]:
            sheet_name = message["text"][19:]  # takes just the sheet name
            spreadsheet.update_sheet(sheet_name)
            print("sheet updated")
        elif "LogisticsBot reload names" in message["text"]:
            spreadsheet.reload_name_conversion()
            print("names reloaded")
        elif "event" in message:  # if msgs has 'event' then we care about it
            event = message["event"]
            if event["type"].startswith("calendar.event.user"):
                answer = event["type"]  # eg not_going.
                nickname = event["data"]["user"]["nickname"]  # GroupMe nickname
                eventName = event["data"]["event"]["name"]  # GroupMe event name
                spreadsheet.change_answer(answer, nickname, eventName)
        new_prams['after_id'] = message["id"]
    time.sleep(60)

import time
import requests
from src import spreadsheet

s_url = 'https://api.groupme.com/v3/groups/44100309/messages'  # smaller url
request_parameters = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO'}
resp_msgs = requests.get(s_url, params=request_parameters).json()['response']['messages']
# The 20 most recent messages, https://dev.groupme.com/docs/v3#messages

new_prams = {
    'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO',
    'after_id': resp_msgs[19]["id"]
}


while 1:
    response = requests.get(s_url, params=new_prams)
    new_msgs = response.json()['response']['messages']
    # gets the most recent events, after the id of the last event called.

    for message in new_msgs:
        if "LogisticsBot sheet" in message["text"]:
            sheet_name = message["text"][19:]  # takes just the sheet name
            spreadsheet.update_sheet(sheet_name)
        # elif "LogisticsBot reload names" in message["text"]:
        #    spreadsheet.reload_names
        # implement this command to reload the name conversion in the sheet.
        elif "event" in message:  # if msgs has 'event' then we care about it
            event = message["event"]
            if "calendar.event.user" in event["type"]:
                answer = event["type"]  # eg not_going.
                nickname = event["data"]["user"]["nickname"]  # GroupMe nickname
                eventName = event["data"]["event"]["name"]  # event name
                spreadsheet.change_answer(answer, nickname, eventName)
        new_prams['after_id'] = message["id"]
    time.sleep(60)

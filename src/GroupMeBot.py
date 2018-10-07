import time as t
import requests as rqsts
from src import spreadsheet

s_url = 'https://api.groupme.com/v3/groups/44100309/messages'  # smaller url
rqst_prams = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO'}
new_prams = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO',
                      'after_id': '0'}

resp_msgs = rqsts.get(s_url, params=rqst_prams).json()['response']['messages']
# The 20 most recent messages, https://dev.groupme.com/docs/v3#messages

new_msgs = rqsts.get(s_url, params=new_prams).json()['response']['messages']
# recent messages, but using the param 'after_id'

new_prams['after_id'] = resp_msgs[19]["id"]


while 1:
    response = rqsts.get(s_url, params=new_prams)
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
            if "event.user" in message["event"]["type"]:  # only event responses have the substring 'event.user'
                ans = event["type"]  # this should be the answer to the event, eg not_going.
                nick = event["data"]["user"]["nickname"]  # this should be the GroupMe nickname
                eventName = event["data"]["event"]["name"]  # this should be the GroupMe events name
                spreadsheet.change_answer(ans, nick, eventName)  # updates the spreadsheet
        new_prams['after_id'] = message["id"]
    t.sleep(60)

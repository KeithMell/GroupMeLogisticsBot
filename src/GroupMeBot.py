import requests
import time as t
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
fullSheet = client.open("RealCopyLogisticsSheet")  # I made a copy of the logistics spreadsheet
sheet_name = 'September 1 to 30'
sheet = fullSheet.worksheet(sheet_name)  # maybe a bot command to change the sheet?
sheet_conversions = fullSheet.worksheet('Name Conversion')

s_url = {'url': 'https://api.groupme.com/v3/groups/44100309/messages', }  # just shrinking the url
request_params = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO'}
new_message_params = {'token': 'V34ln1DMe3q1yZPu8dGWnPhzzoPQxfY61CzNOwXO',
                      'after_id': '0'}

resp_msgs = requests.get(s_url['url'], params=request_params).json()['response']['messages']
# this should just be the 20 most recent messages, https://dev.groupme.com/docs/v3#messages

new_msgs = requests.get(s_url['url'], params=new_message_params).json()['response']['messages']
# recent messages, but using the param 'after_id', so also indexing backwards, oldest = [0]

new_message_params['after_id'] = resp_msgs[19]["id"]


lower_name_conversion = {  # simple dictionary for conversion
    'Karen Mellendorf': 'Karen',
    'Kayla Mellendorf': 'Kayla',
    'Brian Mellendorf': 'Brian',
    'Nora': 'Nora',
    'Keith Mellendorf': 'Keith',
    'Kyle Brown': 'Kyle B'
}
name_conversion = {k: v.upper() for (k, v) in lower_name_conversion.items()}

answerConversion = {  # simple dictionary for conversion
    'calendar.event.user.going': 'Yes',
    'calendar.event.user.not_going': 'No',
    'calendar.event.user.undecided': 'Maybe'
}


def sheet_change_answer(answer, nickname, event_name_lower):
    answer = answerConversion[answer]  # changing the group Me response to 'yes', 'no', or 'maybe'
    if nickname in name_conversion:
        name = name_conversion[nickname]  # Changing group Me names to Spreadsheet Names
    else:
        name = nickname
    event_name = event_name_lower.upper()  # capitalizing the event name
    lower_name_list = sheet.col_values(1)  # the first column of the spreadsheet, has all the names.
    lower_event_list = sheet.row_values(1)  # the first row of the sheet, has all the event names
    name_list = [i.upper() for i in lower_name_list]  # capitalizing the list of name
    event_list = [j.upper() for j in lower_event_list]  # capitalizing the list of events
    if (name in name_list) & (event_name in event_list):
        sheet.update_cell(1 + name_list.index(name), 1 + event_list.index(event_name), answer)
        print(answer, name, event_name)
        print("\n")
    else:
        print("Either name or Event was entered wrong")
        # maybe have a blank sheet that tells when something was entered wrong.


while 1:
    response = requests.get(s_url['url'], params=new_message_params)
    new_msgs = response.json()['response']['messages']
    # gets the most recent events, after the id of the last event called.

    for message in new_msgs:
        if "LogisticsBot sheet" in message["text"]:
            sheet_name = message["text"][19:]
            print(sheet_name)
            sheet = fullSheet.worksheet(sheet_name)  # updating the sheet to be edited
        elif "event" in message:  # if the msgs has an 'event' then we care about it
            event = message["event"]
            if "event.user" in message["event"]["type"]:  # only event responses have the substring 'event.user'
                ans = event["type"]  # this should be the answer to the event, eg not_going.
                nick = event["data"]["user"]["nickname"]  # this should be the GroupMe nickname
                eventName = event["data"]["event"]["name"]  # this should be the GroupMe events name
                sheet_change_answer(ans, nick, eventName)  # this function updates the spreadsheet

        new_message_params['after_id'] = message["id"]

    t.sleep(60)

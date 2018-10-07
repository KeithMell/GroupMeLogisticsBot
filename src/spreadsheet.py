import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
fullSheet = client.open("RealCopyLogisticsSheet")  # copy of the logistics sheet
sheet_name = 'September 1 to 30'
sheet = fullSheet.worksheet(sheet_name)
sheet_conversions = fullSheet.worksheet('Name Conversion')


lower_name_conversion = {  # simple dictionary for conversion
    'Karen Mellendorf': 'Karen',
    'Kayla Mellendorf': 'Kayla',
    'Brian Mellendorf': 'Brian',
    'Nora': 'Nora',
    'Keith Mellendorf': 'Keith',
    'Kyle Brown': 'Kyle B'
}
name_conversion = {k: v.upper() for (k, v) in lower_name_conversion.items()}
# capitalizes the names for easier comparison

answerConversion = {  # simple dictionary for conversion
    'calendar.event.user.going': 'Yes',
    'calendar.event.user.not_going': 'No',
    'calendar.event.user.undecided': 'Maybe'
}


def update_sheet(new_name): # updating the sheet to be edited
    global sheet
    sheet = fullSheet.worksheet(new_name)


def change_answer(answer, nickname, event_name_lower):
    answer = answerConversion[answer]
    # changing the group Me response to 'yes', 'no', or 'maybe'

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
        print(answer, name, event_name, "\n")
    else:
        print("Either name or Event was entered wrong")
        # maybe have a blank sheet that tells when something was entered wrong.

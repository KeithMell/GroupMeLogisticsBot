import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
fullSheet = client.open("RealCopyLogisticsSheet")
sheet = fullSheet.worksheet('September 1 to 30')




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



#
# Maybe use a dict to compare groupMe names to spreadsheet names
#
# name = input("Enter your name? ")
# meeting = input("which meeting you are answering? ")
# response = input("are you attending? ")
name = 'Abigail'
meeting = 'Tuesday Meeting1'
response = 'Yes'
changingsheet(name, response, meeting)
#


nameConversion = {
    'Aaron': 'Aaron Jong',
    'Abigail': 'Abigail Smith',
    'Adi': 'Aditya Prakash',
    'Anish A / Anthony': 'Anish Toomu',
    'Bella': 'Bella Ramoin',
    'Ben': 'Benjamin Beach',
    'Connor': 'Connor Mitchell',
    'Dominic': 'Dominic Seidita',
    'Duncan': 'Duncan Cameron',
}

print(nameConversion['Aaron'])
print(nameConversion['Abigail'])

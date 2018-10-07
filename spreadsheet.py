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


namelist = sheet.col_values(1)
eventlist = sheet.row_values(1)
print(eventlist)
print(namelist)

def changingsheet(person, answer, event):
    if (person in namelist) & (event in eventlist):
        sheet.update_cell(1 + namelist.index(person), 1 + eventlist.index(event), answer)
        print(namelist.index(person))
        print(eventlist.index(event))
        print(answer)
        print(sheet.cell( 1 + namelist.index(person), 1 + eventlist.index(event)))
    else:
        print("Either name or Event was typed wrong")


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

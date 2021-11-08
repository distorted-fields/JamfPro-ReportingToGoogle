# JSS Advanced Search to Google Sheet
# Original concept by Brad Schmidt on 10/8/2015
# Modified by Aaron Hodgson on 3/10/2021
# Requires a Google developer account, project, and key. 

############################################
# Variables
############################################ 

# Enter "Computer" or "Mobile" based on Advanced Search type desired
AdvSrch_Type=""

# ID of the Jamf Pro Advanced Search
AdvSrch_ID="" 

# Name of JSON file should be located in same folder as this script or include the full filepath of it's location
SERVICE_ACCOUNT_FILE = 'keys.json'

workbook_key="" # Google Sheet ID
worksheet_name = "" # Where main data should be imported
date_cell = "" # Tab and cell for updating date/time of last import - IE Summary Page!C2

# JSS Authentication
jss_host = "" # Include https:// leave off port number Example: https://your.jss.com
jss_port = "" # Port number
jss_username = "" # Setup a user with API rights to read Advanced Computer and Mobile Reports as well as Computers and Mobile Devices
jss_password = "" # Password


################################################################
######### You should not have to modify below this line ########
################################################################

################################################################
##################---Importing Libraries---#####################
################################################################
import gspread
import json
import requests
import string
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
################################################################

# Google Sheet API setup
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None 
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

#testing
client = gspread.authorize(creds)
workbook = client.open_by_key(workbook_key)
worksheet = workbook.worksheet(worksheet_name)

# Mobile or Computer Search - set values
def AdvSrch_Type_f(AdvSrch_Type):
    if AdvSrch_Type == "Computer":
        return "advancedcomputersearches","advanced_computer_search","computers"
    if AdvSrch_Type == "Mobile":
        return "advancedmobiledevicesearches","advanced_mobile_device_search","mobile_devices"
    else:
        print('Failed to set AdvSrch_Type properly.\rPlease uncomment AdvSrch_Type = "Computer" or AdvSrch_Type = "Mobile"')

# Get the report data
def getReportData(as_path,as_key,as_rows):
    # Make the request of the JSS API
    r = requests.get(jss_host + ':' + jss_port + '/JSSResource/' + as_path + '/id/' + AdvSrch_ID, headers={'Accept': 'application/json'}, auth=(jss_username,jss_password))
   
    # Get the device data we need
    report_data = r.json()[as_key]

    # Get the header values
    for c in report_data[as_rows]:
        columns = c.keys()

    # Return the data and the headings
    return report_data[as_rows],columns


def publish(report,columns):

    # Clear out existing data from the sheet
    workbook.values_clear(worksheet_name +'!A:Z')

    # Setup the Header row
    # Get the number of columns provided by the Advanced Search
    number_of_columns = len(columns) - 1

    # Set the cell range
    cell_list = worksheet.range('A1:%s1' % string.ascii_uppercase[number_of_columns])

    # Create a list of column header values
    header_data = []
    for header in columns:
        header_data.append(header)

    # Iterates through each value in the list and each cell
    for heading, cell in zip(header_data,cell_list):
        cell.value = heading

    # Update the sheet with column headers
    worksheet.update_cells(cell_list)

    # Prepare the data from the Advanced Search
    search_data = []
    for line in report:
        for header in columns:
            cell = line.get(header)
            search_data.append(cell)

    # Let's see how many rows are in the report
    rows = len(report)

    # Select a range
    cell_list = worksheet.range('A2:%s%s' % (string.ascii_uppercase[number_of_columns],rows + 1))

    # Set the cell value while iterting through values and cells
    for value, cell in zip(search_data,cell_list):
        cell.value = value

    # Update the spreadsheet with the report data
    worksheet.update_cells(cell_list)

# Is it Mobile or Computer, return approprtiate values for parsing the report
# Let's make sure the value was uncommented
try:
    AdvSrch_Type
    as_path,as_key,as_rows = AdvSrch_Type_f(AdvSrch_Type)
except NameError:
    print('Failed to set AdvSrch_Type properly.\rPlease uncomment AdvSrch_Type = "Computer" or AdvSrch_Type = "Mobile"')
    sys.exit(1)



# Get the data from the advanced search
report,columns = getReportData(as_path,as_key,as_rows)

# Publish to Google Sheet
publish(report,columns)


# import todays date marking last update to data
today = datetime.today().strftime('%Y-%m-%d %I:%M%p')
body = [[today]]
result = sheet.values().update(spreadsheetId=workbook_key, range=date_cell, valueInputOption="USER_ENTERED", body={"values":body}).execute()

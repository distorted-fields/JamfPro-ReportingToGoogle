# Jamf To Google erporting

QuickNav:
Create the developer project so you can get the OAuth key
Setup a Google Sheet
Create advanced search
Client (macOS or Linux) that will run the script
Run the script
Automate it!

Create the developer project so you can get the OAuth key
Go to https://console.cloud.google.com/ and sign in
Create a new project
Give the project a name and the following settings: 
Enable the Google Sheets API - https://console.cloud.google.com/apis/api/sheets.googleapis.com
Click on Credentials, Click Add Credentials
Click on Service Account
Create a new account with a meaningful name
Copy the Client ID and email address to a safe location
Create an access key
From the actions menu of the service account select “Manage keys”
Create a new key with json as the key type
The json key should download to your computer - rename it keys.json
The .json file should be saved in the same folder as the python script

Setup a Google Sheet
Sign into drive.google.com as the api user or yourself and create a new sheet.
Share that sheet with the service account user above
Give the Workbook a name
Give the Sheet a name
Copy the spreadsheet key to safe location (Part of the URL that is before /edit )
Looks like this: 1pasdfsBr_8a3anlLDIdiSLENlsdnOK9s7bJqhdGow

Create advanced search
Create an advanced search as desired, 
Copy the id to a safe location (found in the URL - “Searches.html?id=#”)

Client (macOS or Linux) that will run the script
Install python3 command line tools - xcode-select --install 
Run ( sudo pip3 install --upgrade -r /path/to/requirements.txt ) or 
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade gspread
sudo pip3 install --upgrade oauth2client
sudo pip3 install --upgrade google-api-python-client
Modify the script variables 
AdvSrch_Type - Computer or Mobile
Workbook_key - taken from above
AdvSrch_ID - taken from above 
Worksheet_name - where data will be imported
Date_cell (optional) - cell that will keep track of last update timestamp
API information as needed. 

Run the script
Using terminal cd into the directory with comps-JSSToGoogle.py and/or mobile-JSSToGoogle.py
Reminder keys.json should be in this directory as well. 
Run the script with python3 comps-JSSToGoogle.py or python3 mobile-JSSToGoogle.py

Automate it!
In Terminal, use crontab -e to create a new cron job and enter the following settings
 The path should be updated to the relevant location of the script

Use https://crontab.guru/ to customize the schedule

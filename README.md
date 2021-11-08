# Jamf To Google Reporting

*Requires Google Apps for Domain/Education*

### Overview
1. Google Project And Keys
2. Setup A Google Sheet
3. Create A Jamf Advanced Search
4. Set Up The Client (macOS or Linux) That Will Run The Script
5. Modify The Script Variables
6. Run The Script
7. Automate It!

### Google Project and Keys
Create the developer project by going to https://console.cloud.google.com/ and sign in
 1. Create a new project and give it a descriptive name.
 2. Configure the following settings: 
	* Enable the Google Sheets API - https://console.cloud.google.com/apis/api/sheets.googleapis.com
	* Click on Credentials, Click Add Credentials
	* Click on Service Account
		* Create a new account with a meaningful name.
		* Copy the Client ID and email address to a safe location.
		* Create an access key.
	* From the actions menu of the service account select “Manage keys”
		* Create a new key with json as the key type.
		* The json key should download to your computer, rename it keys.json.
		* The keys.json file should be saved in the same folder as the python script later on.

### Setup A Google Sheet
* Sign into drive.google.com as the api user above or yourself and create a new sheet. If you sign in as yourself, then share the sheet with full edit access to the service account above. 
* Give the Workbook a name.
* Give your Import tab/sheet a name.
* Copy the spreadsheet key to safe location 
	* (The key is the part of the URL that is before /edit, usually looks like this: 1pasdfsBr_8a3anlLDIdiSLENlsdnOK9s7bJqhdGow)*

### Create A Jamf Advanced Search
* Create your advanced search as desired, including the desired display fields.
* Copy the search id to a safe location (found in the URL - “Searches.html?id=##”)

### Set Up The Client (macOS or Linux) That Will Run The Script
1. Install python3 command line tools:
	* `xcode-select --install`
2. Install the additional python helpers by downloading the requirements.txt and running this command
	* `sudo pip3 install --upgrade -r /path/to/requirements.txt`
	* You can also install each seperately by running these commands 
		* `sudo pip3 install --upgrade pip`
		* `sudo pip3 install --upgrade gspread`
		* `sudo pip3 install --upgrade oauth2client`
		* `sudo pip3 install --upgrade google-api-python-client`

### Modify The Script Variables
AdvSrch_Type - Computer or Mobile
Workbook_key - taken from above
AdvSrch_ID - taken from above 
Worksheet_name - where data will be imported
Date_cell (optional) - cell that will keep track of last update timestamp
API information as needed. 

### Run The Script
1. Using terminal cd into the directory with jamf-to-google.py
	* `cd /Volumes/path/to/where/scrip/lives`
2. *Reminder keys.json should be in this directory as well, or the script should be updated to point to where it is.*
3. Run the script with 
	* `python3 jamf-to-google.py`

### Automate it!
* In Terminal, use crontab -e to create a new cron job and enter the following settings
	* `*/60 * * * * cd /Volumes/path/to/where/scrip/lives && /usr/bin/python3 jamf-to-google.py`
* Use https://crontab.guru/ to customize the schedule

"""
Basic functionality of Google Sheets API
Acquires OAuth with i2kdesignllc@gmail.com credentials
Requires client_secrets.json file to live in the same directory as this script
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Sheets API
def sheets_setup():
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
	SPREADSHEET_ID = '1kblFk0ApeTzCIxTmksD8kmItaewMoCBNANDfQ3nbh6U'
	RANGE_NAME = 'Account!G2:H'
	# WARNING: ID & PASSWORD MUST RESIDE IN COLUMNS 'G' and 'H'
	#          AS DEFINED ABOVE
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
	                                             range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('ERROR m404: No data found in Google Sheets.')
	return values

def clean_values(values):
	# filters resulting array of values returned from sheets_call_api()
	return [x for x in values if x]
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Define the scope for the Google Sheets API
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Load the credentials from the file
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\Users\\alean\\OneDrive\\Desktop\\Qr Code scanner\\credentials.json", scopes=scope)

# Authorize gspread with the credentials
client = gspread.authorize(creds)

# Open the Google Sheet by its name
sheet = client.open('OFFICIAL REGISTRATION BATCH 99 (trial)').sheet1  # 'sheet1' refers to the first sheet in the file

# Get all values from the second column ("B")
second_column = sheet.col_values(2)  # Column B is the 2nd column

# Print the values in column B
print(second_column)

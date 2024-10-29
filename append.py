'''import pandas as pd
s1 = []
s2 = pd.Series([4, 5, 6])
s3 = pd.Series([4, 5, 6], index=[3,4,5])

s1.append(s3)
print(s1)



Trial that I do not want to delete yet:
import xlsxwriter


data = {
    "name":"hello",
    "name":"nicetomeet you"
}

workbook = xlsxwriter.Workbook("append.xlsx")

worksheet = workbook.add_worksheet("Firstsheet")

worksheet.write(0, 1, "name" )

for index, entry in enumerate(data):
    worksheet.write(index+1, 0, str(index))


 
to do find a way to append and add into the list
before adding into the list make sure to check if it's not part
if it is already there, make an error code saying it's part
if the name is not in the previous list: error name not found

''' 

import pandas as pd
import datetime
import pytz

timezone = pytz.timezone('Asia/Manila')
datetime_pst = datetime.datetime.now(timezone)
current_time = datetime_pst.strftime("%Y-%m-%d %H:%M:%S")


name = ["yana"]
# Data to be added (strings)
data = {'Name': name, 'Ctime': [current_time]}
new_data = pd.DataFrame(data)

# Path to your existing Excel file
file_path = 'append.xlsx'

# Load the Excel writer in append mode, set if_sheet_exists to 'overlay'
with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    # Specify the sheet name
    sheet_name = "Sheet1"
    
    # Write the new data to the sheet, appending it below the last row
    start_row = writer.sheets[sheet_name].max_row  # find the end of the existing data
    new_data.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row)

print("String data added successfully!")

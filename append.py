
import pandas as pd
import datetime
import pytz

timezone = pytz.timezone('Asia/Manila')
datetime_pst = datetime.datetime.now(timezone)
current_time = datetime_pst.strftime("%Y-%m-%d %H:%M:%S")




def log(name):
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
        new_data.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row, header=False)

    print("String data added successfully!")



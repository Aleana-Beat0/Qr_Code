#generates the QR With special Codes 

import pandas as pd 
from creator import createqr
import random
import string
import pandas as pd



def log(name, special_code):
    # Additing the name and special Code
    namea = name + special_code
    banana = ''
    data = {'Name': namea, 'Code': [banana]}
    new_data = pd.DataFrame(data)

    #File where the names with special number will upload
    file_path = 'names_SP.xlsx'

    # Load the Excel writer in append mode, set if_sheet_exists to 'overlay'
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        # Specify the sheet name
        sheet_name = "Sheet1"
        
        # Write the new data to the sheet, appending it below the last row
        start_row = writer.sheets[sheet_name].max_row  # find the end of the existing data
        new_data.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row, header=False)

    #print("String data added successfully!")





#uploading the participants names
sheet=pd.read_excel("names.xlsx", "Sheet1")


for index, r in sheet.iterrows():
    #ensure this is the sheet name
    names = r['Full Name']
    
    #Debugger for names aren't printing
    #print(names)

    #Generates random Strings of code
    chars = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(5))
    #print(random_string)

    approved_names = names + random_string
    #print(names)

    log(names, random_string)
    createqr(approved_names, random_string)







import pandas as pd 
from creator import createqr



# Read a comma separated values (CSV) files into a variable
# as a pandas DataFrame


sheet=pd.read_excel("sheet.xlsx", "Google sheet")

for index, r in sheet.iterrows():
    names = r['Full Name']
    approved_names = names + 'SP99'
    print(approved_names)
    
    createqr(approved_names, 'SP99')






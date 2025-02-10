#Generates the QR without the special code


import pandas as pd 
#make sure to import creator 
from creator import createqr

#File where the names are being saved
sheet=pd.read_excel("sheet.xlsx", "Google sheet")


for index, r in sheet.iterrows():
    names = r['Full Name']
    approved_names = names
    print(approved_names)
    
    createqr(approved_names,'')






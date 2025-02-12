# Events QR Ticketing System

This program will allow you generate QR codes for participants and scans the QR on the day of the event. It uses special code and login time, which allows organizers to track who is joining the event. This is a fast way for participants to register.
This project consists of two different files.

Note: This can only run locally as of the moment. I'm still developing the features where it can be web-based.

## Step 1: Setup
- update all software (python, pip, code editor, etc..)
- create a virtual environment

- Download all necessary requirements
`pip install -r requirements.txt`

## Step 2: Generation of QR Code - ACreation-QR-Code

You can choose either from the program:

[Generates the QR without the special code - It only generates with it's name](https://github.com/Aleana-Beat0/Qr_Code/blob/c4fed838d6ea797334f077ae8394a01c14bb04bb/ACreation_QR_Code/generates_QR._WSP.py)
[Generates the QR WITH the special code](https://github.com/Aleana-Beat0/Qr_Code/blob/main/ACreation_QR_Code/generates_QR_SC.py)

** Getting the participants name: **
This file is for the names of the participants. It can come from the google sheet, google forms, typeforms, or any file that has been converted to an xlsx file. 
````
#uploading the participants names
sheet=pd.read_excel("names.xlsx", "Sheet1")
````

**Names_SP:**

This sheet is for verifying QR codes after they've been created.  It's called "Names_SP," where "SP" stands for "special code."

The special code is a random string of numbers, and by default, it's 5 digits long.  You can change it if you want something more secure.
````
#File where the names with special number will upload
file_path = 'names_SP.xlsx'
````

## Step 2: Scanner_QR_Code - File location where scans the QR
[Scans the generated QR Code](https://github.com/Aleana-Beat0/Qr_Code/blob/main/BScanning_QR_Code/Actual_scanner.py)


It uses OpenCV to look for QR codes with your webcam. When it sees one, it reads the information inside. Then, it checks a list of names (called "names_SP") to see if that person is on the list. It checks every single name to make sure it doesn't miss anyone. If the name and special code match, then that person is welcome to join the party!
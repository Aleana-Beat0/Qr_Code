import pandas as pd 
import cv2
from pyzbar.pyzbar import decode
import numpy as np

#append is more on the time that they came in 
import append

def scan_qr_code():
    global qr_data

    # Start webcam capture
    cap = cv2.VideoCapture(0)  # Change the argument if needed, e.g., 0 for default camera
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Decode QR codes
        qr_codes = decode(frame)
        
        for qr_code in qr_codes:
            # Extract QR code data

            qr_data = qr_code.data.decode('utf-8')

            
            # Draw a rectangle around the QR code
            points = qr_code.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 3)
            
            # Display QR code data on the frame
            cv2.putText(frame, qr_data, (qr_code.rect.left, qr_code.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Once QR code is detected, close the window
            cap.release()
            cv2.destroyAllWindows()
            return qr_data  # Exit the function to stop the program
        
        # Display the frame with the QR code outlined
        cv2.imshow('QR Code Scanner', frame)

        # Press 'q' to quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture and close the window
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
 
    banana = True
    while banana:
        scan_qr_code()


        used_qr_codes = set()

        found_match = False


        #Reminder that the sheet name should be the same 

        #Name of the participants with the special codes
        sheet = pd.read_excel("names_SP.xlsx", "Sheet1")
        
        #log sheet on when the qr got scanned
        logsheet = pd.read_excel("append.xlsx", "Sheet1")

        names = sheet.iloc[:, 0].tolist()
        from colorama import Fore, Style
        print(Fore.WHITE + qr_data)
        print(Style.RESET_ALL)


        if qr_data in names:
            found_match = True
            if qr_data in logsheet['Name'].values:
                print(Fore.RED + 'Error: This QR code has already been used.')
                print(Style.RESET_ALL)
                print("Error: This QR code has already been used.")
                
            else:
                append.log(qr_data)
                print("Horray, welcome!")
            
        else:
            print(Fore.RED + 'You are not part of the party.')
            print(Style.RESET_ALL)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            banana = False
            break










import pandas as pd 
import cv2
from pyzbar.pyzbar import decode
import numpy as np
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


        if cv2.waitKey(1) & 0xFF == ord('q'):
            banana = False
            break



'''
To dos:
idk fix the repetative loop thing cuz it's not stopping
find a way that enables it to stop once it sees the values
'''


'''
#password with settings

        if "SP99" in qr_data:
            print("You are approved")
        else:
            print("You are rejected")

'''








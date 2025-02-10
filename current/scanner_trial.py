import pandas as pd
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import streamlit as st
import append
from io import BytesIO

# Function to scan QR code from an image
def scan_qr_code(frame):
    qr_data = None
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

    return qr_data, frame

# Streamlit app
def main():
    st.title("QR Code Scanner")

    # Upload camera input via Streamlit's camera input
    camera_input = st.camera_input("Scan your QR code")

    if camera_input:
        # Convert the uploaded image to an OpenCV format
        img_bytes = camera_input.getvalue()
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Scan the QR code
        qr_data, frame_with_qr = scan_qr_code(frame)

        # Show the frame with the QR code drawn on it
        _, buffer = cv2.imencode('.jpg', frame_with_qr)
        io_buffer = BytesIO(buffer)
        st.image(io_buffer, caption="QR Code Scan", use_column_width=True)

        if qr_data:
            st.write(f"QR Code Data: {qr_data}")

            # Load the sheets for checking QR code match
            sheet = pd.read_excel("names_SP.xlsx", "Sheet1")
            logsheet = pd.read_excel("append.xlsx", "Sheet1")

            names = sheet.iloc[:, 0].tolist()

            if qr_data in names:
                if qr_data in logsheet['Name'].values:
                    st.error("Error: This QR code has already been used.")
                else:
                    append.log(qr_data)  # Log the QR code data
                    st.success("Hooray, welcome!")
            else:
                st.error("You are not part of the party.")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import tempfile
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import zipfile
from streamlit_gsheets import GSheetsConnection

# Function to create QR code
def createqr(data, rmdata, temp_dir):
    new_data = data.replace(rmdata, '') 
    
    # Create a QR code object with a larger size and higher error correction
    qr = qrcode.QRCode(version=3, box_size=20, border=4, error_correction=qrcode.constants.ERROR_CORRECT_H)

    # Add the data to the QR code object
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code with a black fill color and white background
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a format Pillow can work with (RGBA)
    qr_img = qr_img.convert("RGBA")

    # Define the font and size for the text overlay
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Adjust the font and size as needed
    except IOError:
        # Fallback in case the font is not available
        font = ImageFont.load_default()

    # Get the dimensions of the QR code image
    qr_width, qr_height = qr_img.size

    # Create a new image with extra space for the text
    final_img_height = qr_height + 100  # Add space for text (100px)
    final_img = Image.new('RGB', (qr_width, final_img_height), color="white")

    # Paste the QR code onto the new image
    final_img.paste(qr_img, (0, 0))

    # Prepare the text to be drawn under the QR code
    draw = ImageDraw.Draw(final_img)

    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), new_data, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position to center the text
    text_position = ((qr_width - text_width) // 2, qr_height + 10)

    # Draw the text onto the final image
    draw.text(text_position, new_data, font=font, fill="black")

    # Generate the path to save the image in the temp directory
    temp_image_path = os.path.join(temp_dir, f"{new_data}.png")
    
    # Save the final image
    final_img.save(temp_image_path)

    return temp_image_path


# Function to create a zip file from the QR codes
def create_zip_from_images(image_paths, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_path in image_paths:
            zipf.write(image_path, os.path.basename(image_path))  # Add files to the zip
    return zip_filename


# Streamlit UI
st.title("QR Code Generator - Select Row Range from Google Sheets")

# Input for Google Sheets URL
url = st.text_input("Enter the Google Sheets URL:")

# Button to confirm the link
if st.button("Confirm Link"):
    if url:
        try:
            # Set up the connection to Google Sheets using streamlit_gsheets
            conn = st.connection("gsheets", type=GSheetsConnection)

            # Attempt to read the data from the Google Sheets URL
            data = conn.read(spreadsheet=url)

            # If data is fetched, display it
            if not data.empty:
                st.success("Data successfully loaded from the Google Sheet!")
                st.write(data)  # Display the first few rows of the data
            else:
                st.error("The sheet is empty or there is no valid data.")
        except Exception as e:
            # If there is any error while fetching the data, show an error message
            st.error(f"Failed to load data from the provided Google Sheet link. Error: {e}")
    else:
        st.warning("Please enter a Google Sheets URL.")

# Use session state to remember row selections
if 'start_row' not in st.session_state:
    st.session_state['start_row'] = 0
if 'end_row' not in st.session_state:
    st.session_state['end_row'] = 0

# If the user has provided a valid sheet, show further options to select rows and generate QR codes
if url and st.button("Proceed with QR Code Generation"):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        data = conn.read(spreadsheet=url)

        # Proceed if 'Full Name' column exists
        if 'Full Name' in data.columns:
            # Get the total number of rows
            num_rows = len(data)

            # Persisting the state of start_row and end_row using session_state
            st.session_state['start_row'] = st.number_input(
                "Enter the start row number (inclusive)",
                min_value=0,
                max_value=num_rows - 1,
                value=st.session_state['start_row'],  # Remember the value
                step=1
            )

            st.session_state['end_row'] = st.number_input(
                "Enter the end row number (inclusive)",
                min_value=st.session_state['start_row'],
                max_value=num_rows - 1,
                value=st.session_state['end_row'],  # Remember the value
                step=1
            )

            # Validate the row numbers
            if st.session_state['start_row'] <= st.session_state['end_row']:
                # Create a temporary directory to store the images
                temp_dir = tempfile.mkdtemp()

                # Store paths to all generated images
                image_paths = []

                # Generate the QR codes for each selected row in the range
                for row_index in range(st.session_state['start_row'], st.session_state['end_row'] + 1):
                    name = data.loc[row_index, 'Full Name']
                    image_path = createqr(name.strip(), "", temp_dir)
                    image_paths.append(image_path)

                # Create a zip file containing all the QR code images
                zip_filename = "qr_codes.zip"
                zip_file = create_zip_from_images(image_paths, zip_filename)

                # Allow the user to download the zip file
                with open(zip_file, "rb") as f:
                    st.download_button(
                        label="Download QR Code ZIP",
                        data=f,
                        file_name=zip_filename,
                        mime="application/zip"
                    )

                # Clean up temporary directory (optional)
                for image_path in image_paths:
                    os.remove(image_path)  # Remove individual images
                os.rmdir(temp_dir)  # Remove the temporary directory
            else:
                st.warning("The start row must be less than or equal to the end row.")
        else:
            st.warning("The column 'Full Name' was not found in the Google Sheet.")
    except Exception as e:
        st.error(f"Error: {e}")

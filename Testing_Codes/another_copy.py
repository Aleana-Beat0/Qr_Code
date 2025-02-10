import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile
import streamlit as st
from io import BytesIO
import zipfile

# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

# Define the createqr function
def createqr(data):
    new_data = data
    #new_data = data.replace(rmdata, '')
    
    # Create a QR code object with a larger size and higher error correction
    qr = qrcode.QRCode(version=3, box_size=20, border=4, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Define the font and size for the text overlay
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    qr_width, qr_height = qr_img.size
    final_img_height = qr_height + 100
    final_img = Image.new('RGB', (qr_width, final_img_height), color="white")
    final_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final_img)
    bbox = draw.textbbox((0, 0), new_data, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((qr_width - text_width) // 2, qr_height + 10)
    draw.text(text_position, new_data, font=font, fill="black")

    # Save to the temporary folder
    name_image = os.path.join(temp_dir.name, new_data + ".png")
    final_img.save(name_image)
    return name_image

# Streamlit interface
st.header("QR Code Generator")

# Input form
data = st.text_input("Enter data for the QR code:")
if st.button("Generate QR Code"):
    if data:
        createqr(data)
        st.success("QR Code generated successfully!")
        

# Show files in the temporary directory
files_in_temp = os.listdir(temp_dir.name)
print("something ig", files_in_temp)
if files_in_temp:
    st.write("Generated QR Codes:")
    for file in files_in_temp:
        st.write(f"- {file}")

# Download all files as a ZIP
if st.button("Download All QR Codes as ZIP"):
    
    print("when pressed:", files_in_temp)
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name in files_in_temp:
            file_path = os.path.join(temp_dir.name, file_name)
            zipf.write(file_path, arcname=file_name)
    zip_buffer.seek(0)

    zip_buffer = "bana"
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name="qr_codes.zip",
        mime="application/zip",
    )

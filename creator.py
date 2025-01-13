import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


def createqr(data,rmdata):
    new_data = data.replace(rmdata, '') 
    # Create a QR code object with a larger size and higher error correction
    qr = qrcode.QRCode(version=3, box_size=20, border=4, error_correction=qrcode.constants.ERROR_CORRECT_H)

    # Define the data to be encoded in the QR code


    # Add the data to the QR code object
    qr.add_data(data)

    # Make the QR code
    qr.make(fit=True)

    # Create an image from the QR code with a black fill color and white background
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a format Pillow can work with (RGBA)
    qr_img = qr_img.convert("RGBA")

    # Define the font and size for the text overlay
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # You can adjust the font and size as needed
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

    #renamed path folder to 2
    path_folder = 'C:\\Users\\alean\\OneDrive\\Desktop\\Qr Code scanner'
    name_image = os.path.join(path_folder, new_data + ".png")

    # Save the final image
    final_img.save(name_image)

    # Optionally display the final image
    #final_img.show()


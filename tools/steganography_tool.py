from flask import Blueprint, render_template, request, send_file, current_app
from PIL import Image
import io

steganography_bp = Blueprint('steganography', __name__)

def text_to_bin(message):
    return ''.join(format(ord(i), '08b') for i in message)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if int(c, 2) != 0)

@steganography_bp.route('/')
def index():
    return render_template('tools/steganography_tool.html')

@steganography_bp.route('/hide', methods=['POST'])
def hide():
    image_file = request.files['image']
    message = request.form['message'] + "#####" # Delimiter
    
    img = Image.open(image_file).convert('RGB')
    binary_message = text_to_bin(message)
    data_iter = iter(binary_message)
    
    pixels = list(img.getdata())
    new_pixels = []
    
    try:
        for pixel in pixels:
            r, g, b = pixel
            # Modify Least Significant Bits
            if (bit := next(data_iter, None)) is not None:
                r = (r & ~1) | int(bit)
            if (bit := next(data_iter, None)) is not None:
                g = (g & ~1) | int(bit)
            if (bit := next(data_iter, None)) is not None:
                b = (b & ~1) | int(bit)
            new_pixels.append((r, g, b))
    except StopIteration:
        pass
        
    # Fill remaining pixels
    new_pixels.extend(pixels[len(new_pixels):])
    
    img.putdata(new_pixels)
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    return send_file(byte_io, mimetype='image/png', as_attachment=True, download_name='secret_image.png')

@steganography_bp.route('/extract', methods=['POST'])
def extract():
    image_file = request.files['image']
    img = Image.open(image_file).convert('RGB')
    
    binary_data = ""
    for pixel in img.getdata():
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)
        
    message = bin_to_text(binary_data)
    secret = message.split("#####")[0] # Split by delimiter
    
    return render_template('tools/steganography_tool.html', extracted_text=secret)
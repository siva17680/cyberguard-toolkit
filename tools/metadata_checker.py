from flask import Blueprint, render_template, request
from PIL import Image, ExifTags
import PyPDF2
import os
from werkzeug.utils import secure_filename

metadata_checker_bp = Blueprint('metadata_checker', __name__)

@metadata_checker_bp.route('/', methods=['GET', 'POST'])
def index():
    metadata = {}
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            
            try:
                if ext in ['jpg', 'jpeg', 'png']:
                    image = Image.open(file)
                    exif = image._getexif()
                    if exif:
                        for tag, value in exif.items():
                            decoded = ExifTags.TAGS.get(tag, tag)
                            metadata[decoded] = str(value)
                    
                    # Basic image data if no EXIF
                    metadata['Format'] = image.format
                    metadata['Mode'] = image.mode
                    metadata['Size'] = f"{image.width} x {image.height}"

                elif ext == 'pdf':
                    pdf = PyPDF2.PdfReader(file)
                    info = pdf.metadata
                    if info:
                        for key, value in info.items():
                            metadata[key.replace('/', '')] = str(value)
                    metadata['Pages'] = len(pdf.pages)
            
            except Exception as e:
                metadata['Error'] = f"Could not extract metadata: {str(e)}"

    return render_template('tools/metadata_checker.html', metadata=metadata)
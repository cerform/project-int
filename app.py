from flask import Flask, render_template, request, send_file, render_template_string
from pptx import Presentation
from docx import Document
import os
import mimetypes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


def extract_text_from_pdf(file_path):
    # Implement text extraction from PDF (not provided in this code snippet)
    return ""


def extract_text_from_docx(file_path):
    text = ""
    try:
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text


def extract_images_from_pptx(file_path):
    images = []
    presentation = Presentation(file_path)
    for i, slide in enumerate(presentation.slides):
        image_file = f"slide_{i}.png"
        slide_image = os.path.join(app.root_path, 'templates', 'uploads', 'pptx_images', image_file)
        slide.save(slide_image)  # Save slide as image
        images.append(slide_image)
    return images


def extract_text_from_pptx(file_path):
    text = ""
    try:
        presentation = Presentation(file_path)
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
    except Exception as e:
        print(f"Error extracting text from PPTX: {e}")
    return text


def search_in_text(text, query):
    if text is None:
        return False
    return query.lower() in text.lower()


def get_documents():
    documents = []
    uploads_dir = os.path.join(app.root_path, 'templates', 'uploads')
    for root, dirs, files in os.walk(uploads_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith('.pdf') or file_path.endswith('.docx') or file_path.endswith('.pptx'):
                # Extract category from the folder name containing the file
                category = os.path.basename(os.path.dirname(file_path))
                documents.append({
                    'category': category,
                    'file_name': file_name,
                    'file_path': file_path
                })
    return documents


@app.route('/')
def index():
    categories = [...]  # Your categories list
    files = [...]  # Your files dictionary
    return render_template('index.html', categories=categories, files=files)


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = []
    for document in get_documents():
        text = ""
        if document['file_path'].endswith('.pdf'):
            text = extract_text_from_pdf(document['file_path'])
        elif document['file_path'].endswith('.docx'):
            text = extract_text_from_docx(document['file_path'])
        elif document['file_path'].endswith('.pptx'):
            text = extract_text_from_pptx(document['file_path'])

        if search_in_text(text, query):
            results.append(document)
    return render_template('search_results.html', results=results, query=query)


@app.route('/open/<path:file_path>', methods=['GET'])
def open_or_download_file(file_path):
    # Get the absolute path of the file
    absolute_file_path = os.path.abspath(file_path)

    # Check if the file exists
    if os.path.exists(absolute_file_path):
        # Determine the MIME type of the file
        mime_type, _ = mimetypes.guess_type(absolute_file_path)

        # Check if the file is a text-based file
        if mime_type and mime_type.startswith('text'):
            # Extract text content from supported text-based files (e.g., DOCX, PPTX)
            if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text = extract_text_from_docx(absolute_file_path)
                return render_template_string('<pre>{{ content }}</pre>', content=text)
            elif mime_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                images = extract_text_from_pptx(absolute_file_path)
                return render_template('pptx_preview.html', images=images)
            else:
                # For other text-based files, read the content
                with open(absolute_file_path, 'r') as f:
                    text = f.read()

            # Return the text content as HTML for preview
            return render_template_string('<pre>{{ content }}</pre>', content=text)

        else:
            # Send the file for download
            return send_file(absolute_file_path, mimetype=mime_type, as_attachment=True)
    else:
        # Return a 404 error if the file does not exist
        return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True)

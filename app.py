from flask import Flask, render_template, request, send_file, render_template_string
from pptx import Presentation
from docx import Document
import os
import mimetypes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


# Extract text from PDF function placeholder (implement as needed)
def extract_text_from_pdf(file_path):
    return ""


# Extract text from DOCX files
def extract_text_from_docx(file_path):
    text = ""
    try:
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text


# Extract images from PPTX files (optional functionality)
def extract_images_from_pptx(file_path):
    images = []
    presentation = Presentation(file_path)
    for i, slide in enumerate(presentation.slides):
        image_file = f"slide_{i}.png"
        slide_image = os.path.join(app.root_path, 'templates', 'uploads', 'pptx_images', image_file)
        slide.save(slide_image)  # Save slide as image
        images.append(slide_image)
    return images


# Extract text from PPTX files
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


# Search text in document
def search_in_text(text, query):
    if text is None:
        return False
    return query.lower() in text.lower()


# Get document metadata
def get_documents():
    documents = []
    uploads_dir = os.path.join(app.root_path, 'templates', 'uploads')
    for root, dirs, files in os.walk(uploads_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith('.pdf') or file_path.endswith('.docx') or file_path.endswith('.pptx'):
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
    absolute_file_path = os.path.abspath(file_path)

    if os.path.exists(absolute_file_path):
        mime_type, _ = mimetypes.guess_type(absolute_file_path)

        if mime_type and mime_type.startswith('text'):
            if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text = extract_text_from_docx(absolute_file_path)
                return render_template_string('<pre>{{ content }}</pre>', content=text)
            elif mime_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                images = extract_text_from_pptx(absolute_file_path)
                return render_template('pptx_preview.html', images=images)
            else:
                with open(absolute_file_path, 'r') as f:
                    text = f.read()
            return render_template_string('<pre>{{ content }}</pre>', content=text)
        else:
            return send_file(absolute_file_path, mimetype=mime_type, as_attachment=True)
    else:
        return "File not found", 404


if __name__ == '__main__':
    app.run(debug=True)

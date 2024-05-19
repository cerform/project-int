import os
import mimetypes
from flask import Flask, render_template, request, send_file, render_template_string
from pptx import Presentation
import fitz  # PyMuPDF
from docx import Document

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


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
    documents = get_documents()
    return render_template('index.html', documents=documents)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = []
    for document in get_documents():
        if document['file_path'].endswith('.pdf'):
            text = extract_text_from_pdf(document['file_path'])
        elif document['file_path'].endswith('.docx'):
            text = extract_text_from_docx(document['file_path'])
        else:
            continue
        if search_in_text(text, query):
            results.append(document)
    return render_template('search_results.html', results=results, query=query)

def extract_text_from_pdf(file_path):
    text = ""
    document = fitz.open(file_path)
    for page in document:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    text = ""
    document = Document(file_path)
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def search_in_text(text, query):
    return query.lower() in text.lower()


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
            # Read the text content of the file
            with open(absolute_file_path, 'r') as f:
                file_content = f.read()

            # Return the file content as HTML
            return render_template_string('<pre>{{ content }}</pre>', content=file_content)
        else:
            # Send the file for in-browser viewing
            return send_file(absolute_file_path, mimetype=mime_type)
    else:
        # Return a 404 error if the file does not exist
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)

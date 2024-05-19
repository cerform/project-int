import os
from flask import Flask, render_template, request, redirect, url_for, flash
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
            if file_path.endswith('.pdf') or file_path.endswith('.docx'):
                # Extract category from the folder name containing the file
                category = os.path.basename(os.path.dirname(file_path))
                documents.append({
                    'category': category,
                    'file_name': file_name,
                    'file_path': file_path
                })
    return documents

def save_uploaded_file(file, category):
    uploads_dir = os.path.join(app.root_path, 'templates', 'uploads', category, 'files')
    os.makedirs(uploads_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)
    return file_path

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

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        category = request.form['category']
        new_category = request.form['new_category']

        # If a new category is provided, create the category directory
        if new_category:
            category = new_category
            uploads_dir = os.path.join(app.root_path, 'templates', 'uploads', category)
            os.makedirs(uploads_dir, exist_ok=True)

        # Save the uploaded file
        if file and category:
            file_path = save_uploaded_file(file, category)
            flash('File uploaded successfully', 'success')
            return redirect(url_for('index'))

    return render_template('upload.html')

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

if __name__ == '__main__':
    app.run(debug=True)

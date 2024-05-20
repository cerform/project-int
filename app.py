import os
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename
import mammoth
from pptx import Presentation
import fitz  # PyMuPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('templates/uploads')
app.secret_key = 'supersecretkey'

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx'}

file_index = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def extract_text_from_docx(path):
    with open(path, 'rb') as file:
        document = mammoth.extract_raw_text(file)
    return document.value

def extract_text_from_pptx(path):
    prs = Presentation(path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)

def index_files(upload_folder):
    file_index.clear()
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.txt'):
                content = extract_text_from_txt(file_path)
            elif file.endswith('.pdf'):
                content = extract_text_from_pdf(file_path)
            elif file.endswith('.docx'):
                content = extract_text_from_docx(file_path)
            elif file.endswith('.pptx'):
                content = extract_text_from_pptx(file_path)
            else:
                continue
            relative_path = os.path.relpath(file_path, upload_folder)
            file_index[relative_path] = content
            # Debugging: Log indexed file path
            print(f'Indexed file: {relative_path}')

def search_files(query):
    results = {}
    for file_path, content in file_index.items():
        if query.lower() in content.lower():
            results[file_path] = content
    return results

@app.route('/')
def index():
    categories = {}
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for d in dirs:
            categories[d] = []
        for f in files:
            category = os.path.basename(root)
            if category in categories:
                categories[category].append(f)
    return render_template('index.html', categories=categories)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    search_results = search_files(query)
    return render_template('search_results.html', query=query, results=search_results)

# Function to determine MIME type based on file extension
def get_mime_type(filename):
    return mimetypes.guess_type(filename)[0]

@app.route('/open/<path:file_path>', methods=['GET'])
def open_file(file_path):
    absolute_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file_path))

    print(f"Absolute file path: {absolute_file_path}")

    if os.path.exists(absolute_file_path):
        mime_type, _ = mimetypes.guess_type(absolute_file_path)
        print(f"MIME Type: {mime_type}")

        if mime_type is not None:
            if mime_type.startswith('text'):
                with open(absolute_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return render_template('preview_text.html', content=content)
            elif mime_type == 'application/pdf':
                return send_file(absolute_file_path)
            elif mime_type.startswith('image'):
                return render_template('preview_image.html', file_path=file_path)
            elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return render_template('preview_docx.html', file_path=absolute_file_path)
            elif mime_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                return render_template('preview_pptx.html', file_path=absolute_file_path)
            else:
                return "File type not supported for preview"
        else:
            return "Unknown file type"
    else:
        return "File not found", 404

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        category = request.form['category']
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(category))
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        file_path = os.path.join(category_path, secure_filename(file.filename))
        file.save(file_path)
        index_files(app.config['UPLOAD_FOLDER'])  # Reindex files after upload
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        flash('File type not allowed')
        return redirect(request.url)

if __name__ == '__main__':
    index_files(app.config['UPLOAD_FOLDER'])  # Index files on startup
    app.run(debug=True)

import os
import io
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.abspath('templates/uploads')
app.secret_key = 'supersecretkey'

file_index = {
    'sample.txt': 'This is a sample text file.\nIt contains some text for testing purposes.\n',
    'sample.pdf': 'This is a sample PDF file.\nIt contains some text for testing purposes.\n',
    'sample.docx': 'This is a sample DOCX file.\nIt contains some text for testing purposes.\n',
    'sample.ipynb': '# Sample Notebook\n\nThis is a sample notebook.\n',
}

def extract_text_from_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content

def extract_text_from_pdf(file_path):
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return str(e)

def extract_text_from_docx(file_path):
    try:
        import mammoth
        result = mammoth.extract_raw_text(file_path)
        return result.value.strip()
    except Exception as e:
        return str(e)

def extract_text_from_ipynb(file_path):
    import nbformat
    with open(file_path, 'r') as f:
        notebook = nbformat.read(f, as_version=4)
    cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
    return '\n'.join([cell.source for cell in cells])

def search_files(query):
    results = []
    for filename, content in file_index.items():
        if query in content:
            results.append(filename)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return 'File successfully uploaded'
    return 'Upload failed'

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    results = search_files(query)
    return jsonify({'results': results})

@app.route('/pptx_preview')
def pptx_preview():
    return render_template('pptx_preview.html', title='Slides Content')

if __name__ == '__main__':
    app.run(debug=True)

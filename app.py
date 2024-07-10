import os
import mimetypes
import logging
from flask import Flask, render_template, request, send_file
from pptx import Presentation
import fitz  # PyMuPDF
import nbformat
# Importing necessary libraries

# Configure Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.abspath('templates/uploads')
app.secret_key = 'supersecretkey'

# Set allowed file extensions
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'ipynb'}

# Initialize file index dictionary
file_index = {}

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Helper functions

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def create_directory(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")


def index_files(upload_folder):
    """Index files in the upload folder based on their type."""
    file_index.clear()
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            file_path = os.path.join(root, file)
            content = None
            if file.endswith('.txt'):
                content = extract_text_from_txt(file_path)
            elif file.endswith('.pdf'):
                content = extract_text_from_pdf(file_path)
            elif file.endswith('.docx'):
                content = extract_text_from_docx(file_path)
            elif file.endswith('.pptx'):
                content = extract_text_from_pptx(file_path)
            elif file.endswith('.ipynb'):
                content = extract_text_from_ipynb(file_path)
            if content is not None:
                relative_path = os.path.relpath(file_path, upload_folder)
                file_index[relative_path] = content
                logging.debug(f'Indexed file: {relative_path}')
                new_relative_path = relative_path.replace(" ", "")
                if new_relative_path != relative_path:
                    file_index[new_relative_path] = content
                    logging.debug(f'Reindexed file: {new_relative_path}')


def extract_text_from_txt(path):
    """Extract text from a .txt file."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_text_from_pdf(path):
    """Extract text from a .pdf file."""
    doc = fitz.open(path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)


def extract_text_from_docx(path):
    """Extract text from a .docx file."""
    with open(path, 'rb') as file:
        result = mammoth.extract_raw_text(file)  # Assuming mammoth is properly imported
        return result.value


def extract_text_from_pptx(path):
    """Extract text from a .pptx file."""
    prs = Presentation(path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)


def extract_text_from_ipynb(file_path):
    """Extract text from a .ipynb file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        text = ''
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown' or cell['cell_type'] == 'code':
                text += ''.join(cell['source']) + '\n\n'
        return text


def search_files(query):
    """Search indexed files for a query."""
    results = {}
    for file_path, content in file_index.items():
        if query.lower() in content.lower():
            results[file_path] = content
    return results


# Flask routes

@app.route('/')
def index():
    """Render the main index page."""
    categories = [d for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']) for d in dirs]
    return render_template('index.html', categories=categories)


@app.route('/pptx_player/<path:file_path>')
def pptx_player(file_path):
    """Render a page to play a .pptx file."""
    absolute_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file_path.replace('\\', '/')))
    if os.path.exists(absolute_file_path):
        return render_template('pptx_player.html', pptx_file=file_path)
    else:
        return "File not found", 404


@app.route('/search', methods=['POST'])
def search():
    """Handle search request."""
    query = request.form['query']
    search_results = search_files(query)
    return render_template('search_results.html', query=query, results=search_results)


@app.route('/pptx_preview')
def pptx_preview():
    """Render a preview page for .pptx files."""
    slides_content = get_slides_content()
    return render_template('pptx_preview.html', slides_content=slides_content)


@app.route('/open/<path:file_path>', methods=['GET'])
def open_file(file_path):
    """Handle opening of various file types."""
    file_path = file_path.replace("\\", "/")
    absolute_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file_path.replace('\\', '/')))
    logging.debug(f"Opening file: {absolute_file_path}")

    if os.path.exists(absolute_file_path):
        file_extension = file_path.rsplit('.', 1)[1].lower()
        if file_extension == 'pptx':
            images_dir = os.path.join('static', 'images')
            slides_content = extract_text_and_images_from_pptx(absolute_file_path, images_dir)
            slides_count = len(slides_content)
            logging.debug(f"Slides content: {slides_content}")
            return render_template('pptx_preview.html', slides_content=slides_content,
                                   slides_count=slides_count)
        elif file_extension == 'docx':
            with open(absolute_file_path, 'rb') as f:
                content = mammoth.extract_raw_text(f).value  # Assuming mammoth is properly imported
            return render_template('preview_docx.html', content=content)
        elif file_extension == 'ipynb':
            with open(absolute_file_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
            return render_template('preview_ipynb.html', notebook=notebook)
        else:
            mime_type, _ = mimetypes.guess_type(absolute_file_path)
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
                else:
                    return "File type not supported for preview"
            else:
                return "Unknown file type"
    else:
        return "File not found", 404


@app.route('/preview_ipynb/<path:file_path>', methods=['GET'])
def preview_ipynb(file_path):
    """Render a preview page for .ipynb files."""
    absolute_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file_path))
    if os.path.exists(absolute_file_path):
        with open(absolute_file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        logging.debug(f"Notebook content: {notebook}")  # Debug: Print the notebook content
        return render_template('preview_ipynb.html', notebook=notebook)
    else:
        return "File not found", 404


def extract_text_and_images_from_pptx(file_path, images_dir):
    """Extract text and images from a .pptx file."""
    prs = Presentation(file_path)
    slides_content = []
    slide_index = 0

    for slide in prs.slides:
        slide_index += 1
        slide_content = {'slide_index': slide_index, 'content': '', 'images': []}
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                slide_content['content'] += shape.text + '\n'
            if hasattr(shape, 'image'):
                img_path = os.path.join(images_dir, f'slide_{slide_index}_img_{len(slide_content["images"])}.jpg')
                shape.image.save(img_path)
                slide_content['images'].append(img_path)
        slides_content.append(slide_content)

    return slides_content


def get_slides_content():
    """Retrieve slides content for preview."""
    slides_content = []
    for file_path, content in file_index.items():
        if file_path.endswith('.pptx'):
            slides_content.extend(extract_text_and_images_from_pptx(file_path, 'static/images'))
    return slides_content


# Error handlers

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('error_404.html'), 404


if __name__ == '__main__':
    create_directory(app.config['UPLOAD_FOLDER'])
    index_files(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

import os
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import mammoth
from pptx import Presentation
import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader, select_autoescape, Undefined
import nbformat

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.abspath('templates/uploads')
app.secret_key = 'supersecretkey'
file_index = {}

# Create a custom Jinja environment with enumerate function available
custom_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']),
    undefined=Undefined
)
custom_env.globals['enumerate'] = enumerate  # Pass the enumerate function to the Jinja environment

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'ipynb'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_text_and_images_from_pptx(file_path, uploads_dir):
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    prs = Presentation(file_path)
    slides_content = []

    for slide_index, slide in enumerate(prs.slides):
        slide_content = []
        for shape_index, shape in enumerate(slide.shapes):
            if shape.has_text_frame and shape.text_frame.text.strip():
                slide_content.append({'type': 'text', 'content': shape.text_frame.text})
                print(f"Extracted text from slide {slide_index + 1}, shape {shape_index + 1}: {shape.text_frame.text}")

            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:  # Placeholder for Picture
                image = shape.image
                category = os.path.basename(os.path.dirname(file_path))
                category_dir = os.path.join(uploads_dir, secure_filename(category))
                create_directory(category_dir)  # Ensure the category directory exists
                image_path = os.path.join(category_dir, f"slide_{slide_index + 1}_image_{shape_index + 1}.png")
                with open(image_path, 'wb') as img_file:
                    img_file.write(image.blob)
                relative_image_path = os.path.relpath(image_path, 'static')
                slide_content.append({'type': 'image', 'content': relative_image_path})
                print(f"Saved image from slide {slide_index + 1}, shape {shape_index + 1}: {relative_image_path}")

        slides_content.append({'slide_index': slide_index, 'content': slide_content})

    return slides_content


def create_directory(directory):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


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
        result = mammoth.extract_raw_text(file)
        return result.value


def extract_text_from_pptx(path):
    prs = Presentation(path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)


# Function to extract text from IPYNB files
def extract_text_from_ipynb(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        text = ''
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown':
                text += ''.join(cell['source']) + '\n\n'
            elif cell['cell_type'] == 'code':
                text += ''.join(cell['source']) + '\n\n'
        return text


def index_files(upload_folder):
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
                # Debugging: Log indexed file path
                print(f'Indexed file: {relative_path}')

                # Remove whitespace from the filename
                new_relative_path = relative_path.replace(" ", "")
                if new_relative_path != relative_path:
                    file_index[new_relative_path] = content
                    # Debugging: Log indexed file path after whitespace removal
                    print(f'Reindexed file: {new_relative_path}')


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

    # Enumerate the categories before passing them to the template
    enumerated_categories = [(index, category) for index, category in enumerate(categories)]

    # Create a custom Jinja environment with enumerate function available
    custom_env = Environment(loader=FileSystemLoader('templates'),
                             autoescape=select_autoescape(['html', 'xml']),
                             undefined=Undefined)
    return render_template('index.html', categories=enumerated_categories, env=custom_env)


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
    # Replace backslashes with forward slashes in the file path
    file_path = file_path.replace("\\", "/")

    # Update this line to replace backslashes with forward slashes in the file path
    absolute_file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], file_path.replace('\\', '/')))
    print(f"Opening file: {absolute_file_path}")

    if os.path.exists(absolute_file_path):
        file_extension = file_path.rsplit('.', 1)[1].lower()
        if file_extension == 'pptx':
            images_dir = os.path.join('static', 'images')
            slides_content = extract_text_and_images_from_pptx(absolute_file_path, images_dir)
            print(f"Slides content: {slides_content}")
            return render_template('pptx_preview.html', slides_content=slides_content, enumerate=enumerate)
        elif file_extension == 'docx':
            with open(absolute_file_path, 'rb') as f:
                content = mammoth.extract_raw_text(f).value
            return render_template('preview_text.html', content=content)
        elif file_extension == 'ipynb':
            content = extract_text_from_ipynb(absolute_file_path)
            return render_template('ipynb_preview.html', content=content)
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



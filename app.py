import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pptx import Presentation
import fitz  # PyMuPDF
from docx import Document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for notes
notes = []

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/note/<int:note_id>')
def note_detail(note_id):
    note = notes[note_id]
    return render_template('note.html', note=note, note_id=note_id)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notes.append({'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template('note.html', note={'title': '', 'content': ''}, note_id=-1)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'POST':
        notes[note_id]['title'] = request.form['title']
        notes[note_id]['content'] = request.form['content']
        return redirect(url_for('index'))
    note = notes[note_id]
    return render_template('note.html', note=note, note_id=note_id)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    notes.pop(note_id)
    return redirect(url_for('index'))

def extract_text_from_pdf(file_path):
    text = ""
    document = fitz.open(file_path)
    for page in document:
        text += page.get_text()
    return text

def extract_text_from_pptx(file_path):
    text = ""
    presentation = Presentation(file_path)
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text += run.text + " "
    return text

def extract_text_from_docx(file_path):
    text = ""
    document = Document(file_path)
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def search_in_text(text, query):
    return [line for line in text.split('\n') if query.lower() in line.lower()]

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        query = request.form['query']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.pptx'):
            text = extract_text_from_pptx(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            return "Unsupported file type", 400

        results = search_in_text(text, query)
        return render_template('search_results.html', results=results, query=query)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

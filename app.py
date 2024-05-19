from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

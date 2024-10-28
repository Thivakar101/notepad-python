from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for notes
notes = []

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    filtered_notes = [note for note in notes if search_query.lower() in note['title'].lower() or search_query.lower() in note['content'].lower()]
    return render_template('index.html', notes=filtered_notes, search_query=search_query)

@app.route('/add_note', methods=['POST'])
def add_note():
    note_title = request.form.get('note_title')
    note_content = request.form.get('note_content')
    note_tags = request.form.get('note_tags').split(',')
    if note_title and note_content:
        note = {
            'title': note_title,
            'content': note_content,
            'tags': [tag.strip() for tag in note_tags if tag.strip()],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        notes.append(note)
    return redirect(url_for('index'))

@app.route('/edit_note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    if 0 <= note_id < len(notes):
        note_title = request.form.get('note_title')
        note_content = request.form.get('note_content')
        note_tags = request.form.get('note_tags').split(',')
        notes[note_id]['title'] = note_title
        notes[note_id]['content'] = note_content
        notes[note_id]['tags'] = [tag.strip() for tag in note_tags if tag.strip()]
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 0 <= note_id < len(notes):
        notes.pop(note_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

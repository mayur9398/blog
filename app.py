from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM blogs').fetchall()
    conn.close()
    return render_template('index.html', blogs=blogs)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']

        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = get_db_connection()
        conn.execute('INSERT INTO blogs (title, content, image) VALUES (?, ?, ?)',
                     (title, content, image_filename))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/view/<int:id>', methods=('GET', 'POST'))
def view(id):
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE id = ?', (id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE blog_id = ?', (id,)).fetchall()

    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        conn.execute('INSERT INTO comments (blog_id, name, comment) VALUES (?, ?, ?)',
                     (id, name, comment))
        conn.commit()
        comments = conn.execute('SELECT * FROM comments WHERE blog_id = ?', (id,)).fetchall()

    conn.close()
    return render_template('view.html', blog=blog, comments=comments)

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        image_filename = blog['image']

        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn.execute('UPDATE blogs SET title = ?, content = ?, image = ? WHERE id = ?',
                     (title, content, image_filename, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', blog=blog)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM blogs WHERE id = ?', (id,))
    conn.execute('DELETE FROM comments WHERE blog_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

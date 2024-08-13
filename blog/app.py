import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.exceptions import abort
#------------------------------------------------------------------------------------------------------------
# Python Flask Blog
#
# Web based blog built with Python and Flask.
#
# Reference:
#   https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
#
# Usage:
#   $ python app.py
#   $ command google-chrome 127.0.0.1:5000
#   OR
#   $ make 
#------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Example function.
# 127.0.0.1:5000/success/<enter name here>
@app.route('/success/<name>')
def success(name):
    return 'Welcome %s' % name

@app.route('/math', methods =["GET", "POST"])
def test():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form 
       last_name = request.form.get("lname") 

       message = "Hello, " + first_name + " " + last_name

       return render_template("math.html", message=message)
    
    return render_template('math.html')

# Run the main index file in the home directory.
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Establish a database connection.
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get the posts from the database.
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# Create a new blog post.
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

# Edit an existing post	command google-chrome 127.0.0.1:5000
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# Delete a blog post.
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# Main driver.
if __name__=='__main__':
    app.run(debug=True)
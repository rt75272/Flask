import sqlite3
# -------------------------------------------------------------------
# Init Database Connection
#
# Builds up and connects to a database. Creates database connection
# file called database.db.
#
# Usage:
#   $ python init_db.py
# -------------------------------------------------------------------
# Connect to database and create connection file.
connection = sqlite3.connect('database.db')

# Open, read, and run the database's schema sql file.
with open('schema.sql') as f:
    connection.executescript(f.read())

# Database cursor.
cur = connection.cursor()

# Generate 1st post.
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

# Generate 2nd post.
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

# Commit to database.
connection.commit()
connection.close()

from flask import Flask, render_template, request, Markup, g
import sqlite3

# --- App Setup ---
app = Flask(__name__)

# --- Database Configuration ---
DATABASE = 'database.db'

def get_db():
    """
    Gets the database connection from the application context.
    If a connection doesn't exist, it creates one.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Allows accessing columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with a schema and some sample data."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("Initialized the database.")

# Command to run from the terminal to initialize the DB: flask init-db
@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    init_db()

# --- Routes and Vulnerabilities ---

@app.route('/')
def index():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    VULNERABILITY: Weak Authentication.
    Handles user login. The password is 'password'.
    """
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # This is a very weak authentication check
        if username == 'admin' and password == 'password':
            return render_template('login.html', message='Login Successful! Welcome, admin.')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/search')
def search():
    """
    VULNERABILITY: Reflected Cross-Site Scripting (XSS).
    The 'q' parameter is rendered directly into the template without sanitization.
    """
    query = request.args.get('q', '')
    # Using Markup() or the |safe filter in Jinja2 tells the template engine
    # that the content is safe to render as HTML, thus allowing XSS.
    # A safe implementation would escape this content.
    results = Markup(f"<p class='mt-2 text-gray-300'>You searched for: {query}</p>") if query else ''
    return render_template('search.html', results=results)

@app.route('/products')
def products():
    """
    VULNERABILITY: SQL Injection.
    The 'category' parameter is directly embedded into the SQL query string.
    """
    category = request.args.get('category')
    db = get_db()
    
    # This is the vulnerable part. The input is not parameterized.
    # An attacker can manipulate the query.
    query = "SELECT name, description, price FROM products"
    if category:
        query += f" WHERE category = '{category}'"
    
    try:
        cursor = db.execute(query)
        product_list = cursor.fetchall()
    except sqlite3.Error as e:
        # If the SQL is invalid, show the error
        product_list = []
        query = f"SQL Error: {e}\n\nYour malformed query was:\n{query}"

    return render_template('products.html', products=product_list, query=query)

@app.route('/feedback')
def feedback():
    """Renders the feedback page."""
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
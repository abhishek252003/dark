
# Vulnerable Flask Website for Educational & WAF Testing

This project contains a simple Flask-powered website with intentional vulnerabilities, designed for educational purposes and for testing a local Web Application Firewall (WAF).

**DISCLAIMER: This website is intentionally insecure. DO NOT deploy it on a public-facing server. Use it only in a controlled, local environment for testing.**

## Vulnerabilities Included

1.  **Reflected Cross-Site Scripting (XSS)**
    * **Location:** `/search` route (`templates/search.html`)
    * **How it works:** The search term from the URL parameter `q` is rendered directly into the page's HTML without sanitization.
    * **Test Payload:** `/search?q=<script>alert('XSS')</script>`

2.  **SQL Injection (SQLi)**
    * **Location:** `/products` route (`templates/products.html`)
    * **How it works:** The `category` URL parameter is concatenated directly into the SQL query string, allowing an attacker to manipulate the database query.
    * **Test Payload:** `/products?category=' OR '1'='1`

3.  **Weak Authentication**
    * **Location:** `/login` route (`templates/login.html`)
    * **How it works:** The login form accepts a simple, common password (`password`), making it easy to guess or brute-force.

## How to Run the Application

### Step 1: Create the File Structure

You need to create the following folder and file structure, and copy the code from the blocks above into the corresponding files.

```
vulnerable-app/
├── app.py
├── schema.sql
└── templates/
    ├── layout.html
    ├── index.html
    ├── login.html
    ├── search.html
    ├── products.html
    └── feedback.html
```

### Step 2: Install Dependencies

You need Python and Flask installed.

1.  Open a terminal or command prompt.
2.  Navigate into the `vulnerable-app` directory.
3.  (Recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  Install Flask:
    ```bash
    pip install Flask
    ```

### Step 3: Initialize the Database

Before running the app for the first time, you need to create the database file.

1.  In your terminal (inside the `vulnerable-app` directory), run:
    ```bash
    flask init-db
    ```
2.  You should see a message "Initialized the database." and a new file `database.db` will appear.

### Step 4: Run the Flask App

1.  In your terminal, run the following command:
    ```bash
    flask run
    ```
2.  This will start the development server, usually on `http://127.0.0.1:5000`. Open this address in your browser to see the site.

## How to Host on the Dark Web (for local testing)

Follow these steps to run this Flask application as a Tor hidden service on your local machine.

1.  **Install Tor:** Follow the official instructions for your operating system from the [Tor Project website](https://www.torproject.org/download/).

2.  **Configure Tor for a Hidden Service:**
    * Open the Tor configuration file (usually `/etc/tor/torrc`).
    * Add the following lines. This tells Tor to create a hidden service and forward its traffic to your local Flask app running on port 5000.
        ```
        HiddenServiceDir /var/lib/tor/flask_hidden_service/
        HiddenServicePort 80 127.0.0.1:5000
        ```

3.  **Restart Tor** to apply the changes:
    ```bash
    sudo systemctl restart tor
    ```

4.  **Get Your .onion Address:**
    * View the contents of the `hostname` file to find your unique `.onion` address:
        ```bash
        sudo cat /var/lib/tor/flask_hidden_service/hostname
        ```
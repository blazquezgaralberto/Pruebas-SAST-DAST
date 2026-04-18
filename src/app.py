"""
Demo Flask application — GitHub Advanced Security Demo
ADVERTENCIA: Este archivo contiene vulnerabilidades INTENCIONALES con fines educativos.
CodeQL debería detectar todas las vulnerabilidades marcadas con [VULN].
"""

import sqlite3
import subprocess
import os
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

DB_PATH = "demo.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password', 'user')")
    conn.commit()
    conn.close()


# [VULN-1] SQL Injection — CodeQL: py/sql-injection
# El input del usuario se concatena directamente en la query SQL.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        # VULNERABLE: nunca concatenar input del usuario en queries SQL
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor = conn.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Bienvenido, {user[1]}!"
        return "Credenciales incorrectas", 401

    return render_template_string("""
        <form method="POST">
            <input name="username" placeholder="Usuario">
            <input name="password" type="password" placeholder="Contraseña">
            <button type="submit">Entrar</button>
        </form>
    """)


# [VULN-2] Reflected XSS — CodeQL: py/reflected-xss
# El parámetro 'name' se inserta en el HTML sin sanitizar.
@app.route("/search")
def search():
    query = request.args.get("q", "")
    # VULNERABLE: render_template_string con input sin escapar
    template = f"<h1>Resultados para: {query}</h1>"
    return render_template_string(template)


# [VULN-3] Command Injection — CodeQL: py/command-injection
# El input del usuario se pasa directamente a subprocess.
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # VULNERABLE: nunca pasar input del usuario a shell=True
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout}</pre>"


# [VULN-4] Path Traversal — CodeQL: py/path-injection
# El usuario puede acceder a archivos fuera del directorio permitido.
@app.route("/file")
def read_file():
    filename = request.args.get("name", "")
    # VULNERABLE: no se valida ni normaliza el path
    file_path = os.path.join("uploads", filename)
    try:
        with open(file_path, "r") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "Archivo no encontrado", 404


# [VULN-5] Open Redirect — CodeQL: py/url-redirection
# El usuario controla la URL de redirección.
@app.route("/redirect")
def open_redirect():
    next_url = request.args.get("next", "/")
    # VULNERABLE: redirigir a una URL controlada por el usuario
    return redirect(next_url)


if __name__ == "__main__":
    init_db()
    # VULNERABLE: debug=True expone el debugger de Werkzeug en producción
    app.run(debug=True, host="0.0.0.0", port=5000)

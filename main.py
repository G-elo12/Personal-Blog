from flask import Flask, render_template, abort, request, redirect, url_for, session, flash
from functools import wraps
from db_json import dbJson
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secreto'

app.permanent_session_lifetime = timedelta(days=7)

db = dbJson()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get("password")
        if password == 'baketaso5':
            session.permanent = True
            session['logged_in'] = True
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Contraseña incorrecta. Inténtalo de nuevo.", "danger")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Has cerrado sesión", "info")
    return redirect(url_for('index'))

@app.route('/')
def index():
    articles = db.load_data()
    return render_template("index.html", articles=articles)

@app.route('/<int:id>')
def get_article(id):
    article = db.data_for_id(id)
    if not article:
        abort(404) 
    return render_template("article.html", article=article)

@app.route('/dashboard')
@login_required
def dashboard():
    articles = db.load_data()
    return render_template("dashboard.html", articles=articles)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            title = request.form['title']
            body = request.form["body"]
            date = request.form["date"]
            db.add_data(title=title, body=body, date=date)
            flash("Artículo agregado correctamente", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error al agregar los datos: {str(e)}", "error")
            return redirect(url_for('add'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    article = db.data_for_id(id)
    if not article:
        flash("Artículo no encontrado", "danger")
        return redirect(url_for("dashboard"))
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            body = request.form["body"]
            date = request.form["date"]
            db.update_data(id, title=title, body=body)
            flash("Artículo actualizado correctamente", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error al actualizar los datos: {str(e)}", "error")
            print("error")
            return redirect(url_for('edit', id=id))
    
    return render_template("edit.html", article=article)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    article = db.data_for_id(id)
    if article:
        db.delete(id)
        flash("Artículo eliminado exitosamente", "success")
    else:
        flash("Artículo no encontrado", "danger")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)

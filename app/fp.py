from flask import Flask, redirect, url_for, render_template, request, session
from . import app

@app.route('/home')
def index1():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Your login route and other routes here
@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))
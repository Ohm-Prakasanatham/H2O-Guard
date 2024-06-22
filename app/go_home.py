from flask import Flask, redirect, url_for, render_template, request, session
from . import app

@app.route("/go_home")
def go_home():
    return redirect(url_for("index1")) 

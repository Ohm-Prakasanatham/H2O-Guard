from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=1)

from . import goal1, goal2, goal3, goal4, goal5,fp ,login,go_home

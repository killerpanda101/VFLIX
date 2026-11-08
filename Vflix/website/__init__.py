from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

app = Flask(__name__)
# Set SECRET_KEY in the environment for stable sessions across restarts.
# Falls back to a random per-process key (sessions reset on restart).
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'site.db')
db = SQLAlchemy(app)
		
from website import routes



   
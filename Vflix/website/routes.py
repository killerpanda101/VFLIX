from functools import wraps
import hmac
from flask import render_template, url_for, flash, redirect, request, abort, session
from werkzeug.utils import secure_filename
from website import app, db
from website.form import AddMovieForm, RemoveMovieForm
from website.models import Movies
from PIL import Image 
import os


ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please log in first', 'danger')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def save_picture(form_picture):
    # Never trust the client-supplied filename (path traversal)
    filename = secure_filename(form_picture.filename or '')
    if os.path.splitext(filename)[1].lower() not in ALLOWED_EXTENSIONS:
        abort(400, 'Unsupported image type')
    pics_dir = os.path.join(app.root_path, 'static', 'pics')
    os.makedirs(pics_dir, exist_ok=True)
    picture_path = os.path.join(pics_dir, filename)
    output_size = (280, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return filename


@app.route("/")
def home():
	movies = Movies.query.all()
	return render_template("home.html", movies = movies)  


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		# Credentials come from the environment; login is disabled if unset.
		admin_user = os.environ.get('ADMIN_USER')
		admin_pass = os.environ.get('ADMIN_PASSWORD')
		email = request.form.get('email', '')
		password = request.form.get('password', '')
		if (admin_user and admin_pass
				and hmac.compare_digest(email.encode(), admin_user.encode())
				and hmac.compare_digest(password.encode(), admin_pass.encode())):
			session['is_admin'] = True
			return redirect(url_for('form_add'))
		else:
			flash('Wrong account details', 'danger')
	return render_template("login.html")


@app.route("/form_add", methods=['GET', 'POST'])
@admin_required
def form_add():
	form = AddMovieForm()
	if request.method == 'POST':
		title = request.form.get('name')
		description = request.form.get('description')
		link = request.form.get('link')
		picture_file = save_picture(form.picture.data)
		movie = Movies(title=title, description=description, photo=picture_file, link=link)
		db.session.add(movie)
		db.session.commit()
		flash("Movie added to the db", 'success')        

	return render_template("form_add.html", form=form)    

@app.route("/form_remove", methods=['GET', 'POST'])
@admin_required
def form_remove():
	form = RemoveMovieForm()
	if request.method == 'POST':
		title = request.form.get('name')
		movie = Movies.query.filter_by(title=title).first()
		if(movie):
			db.session.delete(movie)
			db.session.commit()
			flash("Movie deleted", "success")	 		
		else:
			flash("No such movie in the database", "danger")

        
	return render_template("form_remove.html", form=form)        

@app.route("/database")
def database():
	movies = Movies.query.all()
	print(movies)
	return render_template("database.html", movies = movies)
    
@app.route("/player")
def playmovie():
	return render_template("player.html")
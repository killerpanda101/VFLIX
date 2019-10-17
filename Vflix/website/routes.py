from flask import render_template, url_for, flash, redirect, request, abort
from website import app, db
from website.form import AddMovieForm, RemoveMovieForm
from website.models import Movies
from PIL import Image 
import os


def save_picture(form_picture):
    picture_path = os.path.join(app.root_path, "static\\pics", form_picture.filename)
    output_size = (280, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return form_picture.filename


@app.route("/")
def home():
	movies = Movies.query.all()
	return render_template("home.html", movies = movies)  


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		if(request.form['password'] == "123" and request.form['email'] == "admin"):
			return redirect(url_for('form_add'))
		else:
			flash('Wrong account details', 'danger')
	return render_template("login.html")


@app.route("/form_add", methods=['GET', 'POST'])
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
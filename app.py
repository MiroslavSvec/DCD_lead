import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

"""
app config

"""

app = Flask(__name__)

# MongoDB config

app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Collections

users_collection = mongo.db.users
recipes_collection = mongo.db.recipes






@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")


""" 
Documents with pagination
"""

@app.route('/documents')
def documents():
	# The URL looks something like 
	# /documents?limit=6&offset=0
	 
	# Request the limit (in the example URL == 6)	
	p_limit = int(request.args['limit'])

	# Request the offset (in the example URL == 0)	
	p_offset = int(request.args['offset'])
	
	# Prevent user to enter pages with negative values (server error)
	# only if he manually enters the value to URL
	if p_offset < 0:
		p_offset = 0

	# Prevent user to enter pages with values over the collection count(server error)
	# only if he manually enters the value to URL
	num_results = recipes_collection.find().count(),
	if p_offset > num_results:
		p_offset = num_results

	# Send the query with limit and offset taken from args
	recipes = recipes_collection.find().limit(p_limit).skip(p_offset)

	args = {
		"p_limit" : p_limit,
		"p_offset" : p_offset,
		"num_results" : num_results,
		"next_url" : f"/documents?limit={str(p_limit)}&offset={str(p_offset + p_limit)}",
		"prev_url" : f"/documents?limit={str(p_limit)}&offset={str(p_offset - p_limit)}",
		"recipes" : recipes
	}
	return render_template("documents.html", args=args)




"""
User AUTH
"""


# Login
@app.route('/login', methods=['GET'])
def login():
	# Check if user is not logged in already
	if 'user' in session:
		user_in_db = users_collection.find_one({"username": session['user']})
		if user_in_db:
			# If so redirect user to his profile
			flash("You are logged in already!")
			return redirect(url_for('profile', user=user_in_db['username']))
	else:
		# Render the page for user to be able to log in
		return render_template("login.html")

# Check user login details from login form
@app.route('/user_auth', methods=['POST'])
def user_auth():
	form = request.form.to_dict()
	user_in_db = users_collection.find_one({"username": form['username']})
	# Check for user in database
	if user_in_db:
		# If passwords match (hashed / real password)
		if check_password_hash(user_in_db['password'], form['user_password']):
			# Log user in (add to session)
			session['user'] = form['username']
			# If the user is admin redirect him to admin area
			if session['user'] == "admin":
				return redirect(url_for('admin'))
			else:
				flash("You were logged in!")
				return redirect(url_for('profile', user=user_in_db['username']))
			
		else:
			flash("Wrong password or user name!")
			return redirect(url_for('login'))
	else:
		flash("You must be registered!")
		return redirect(url_for('register'))

# Sign up
@app.route('/register', methods=['GET', 'POST'])
def register():
	# Check if user is not logged in already
	if 'user' in session:
		flash('You are already sign in!')
		return redirect(url_for('index'))
	if request.method == 'POST':
		form = request.form.to_dict()
		# Check if the password and password1 actualy match 
		if form['user_password'] == form['user_password1']:
			# If so try to find the user in db
			user = users_collection.find_one({"username" : form['username']})
			if user:
				flash(f"{form['username']} already exists!")
				return redirect(url_for('register'))
			# If user does not exist register new user
			else:				
				# Hash password
				hash_pass = generate_password_hash(form['user_password'])
				#Create new user with hashed password
				users_collection.insert_one(
					{
						'username': form['username'],
						'email': form['email'],
						'password': hash_pass
					}
				)
				# Check if user is actualy saved
				user_in_db = users_collection.find_one({"username": form['username']})
				if user_in_db:
					# Log user in (add to session)
					session['user'] = user_in_db['username']
					return redirect(url_for('profile', user=user_in_db['username']))
				else:
					flash("There was a problem savaing your profile")
					return redirect(url_for('register'))

		else:
			flash("Passwords dont match!")
			return redirect(url_for('register'))
		
	return render_template("register.html")

# Log out
@app.route('/logout')
def logout():
	# Clear the session
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('index'))

# Profile Page
@app.route('/profile/<user>')
def profile(user): 
	# Check if user is logged in
	if 'user' in session:
		# If so get the user and pass him to template for now
		user_in_db = users_collection.find_one({"username": user})
		return render_template('profile.html', user=user_in_db)
	else:
		flash("You must be logged in!")
		return redirect(url_for('index'))

# Admin area
@app.route('/admin')
def admin():
	if 'user' in session:
		if session['user'] == "admin":
			return render_template('admin.html')
		else:
			flash('Only Admins can access this page!')
			return redirect(url_for('index'))
	else:
		flash('You must be logged')
		return redirect(url_for('index'))

	




if __name__ == '__main__':
    if os.environ.get("DEVELOPMENT"):
        app.run(host=os.environ.get('IP'),
                port=os.environ.get('PORT'),
                debug=True)
    else:
        app.run(host=os.environ.get('IP'),
                port=os.environ.get('PORT'),
                debug=False)

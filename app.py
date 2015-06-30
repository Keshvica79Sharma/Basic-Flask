# A VERY BASIC FLASK APPLICATION 

# Since this is only for begginers, you fill find some things (I have marked) that you would want to change when your app grows. But these things are important to 
# understand what happens under the shade.

# All imports can be done together , i have done this for readability
from flask import Flask #Import Flask class from flask module
from flask import render_template #To render html templates
from flask import redirect #Instead of rendering a html, redirect to another function 
from flask import flash #To show flash messages , both errors or informative on the html template
from flask import request #To handle GET/POST request and form values
from flask import session # To maintain user sessions


app = Flask(__name__) #app is an instance of the Flask class
app.secret_key = 'my_secret' # Secret key for session cookie

##########################################################################################
# Login required function : This will protect the routes e.g dashboard to be accessed without loggin in
###########################################################################################
from functools import wraps
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'loggedin' in session:
			return f(*args,**kwargs)
		else:
			flash("You need to login first")
			return redirect('/login')
	return wrap


@app.route('/') # Decorator that specifies the function that gets executed at a specific route
def index(): # Default method is GET (NO NEED TO SPECIFY)
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		mobile = request.form['mobile']
		otp    = request.form['otp']
		# :::NOTE::: this is a very poor way of doing this (only for begginers) , In future we will replace this with a database query and a seperate function.
		if mobile == '9999999999' and otp == '1111':
			###########################################################################################################################################
			# If the user is authenticated, set a session key in the session dictionary as True. This is to indicate flask that a user has logged in
			###########################################################################################################################################
			session['loggedin'] = True # SET the session key to True
			flash('You have been logged in')
			return redirect('/dashboard')
		else:
			flash('Invalid credentials. Please try again.')
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard(): #Later you would want to show the data for which user has logged in.
	return render_template('dashboard.html')

@app.route('/logout') # Whenever someone hits the logout button
def logout():
	session.pop('loggedin',None) # Remove the session key on logout
	flash('You have been logged out')
        return redirect('/login')

if __name__ == '__main__':
	app.run(debug=True)

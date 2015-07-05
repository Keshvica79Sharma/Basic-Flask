# Chapter 2 : FLASK APPLICATION WITH Sqlite database and Unit Tests:::

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

########################################################################
# Integrating sqlite database
import sqlite3
app.database = "myfirstdb.db" #the database you created with the sqlite.py file
from flask import g # An object in flask used to store temporary objects
def connect_db(): 
	return sqlite3.connect(app.database) #return the connection oject

#########################################################################
#########################################################################
# Login required function : This will protect the routes e.g dashboard to be accessed without loggin in
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
########################################################################

@app.route('/') # Decorator that specifies the function that gets executed at a specific route
def index(): # Default method is GET (NO NEED TO SPECIFY)
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		fmobile = request.form['mobile'] # form values
		fotp    = request.form['otp']
		# :::NOTE::: Changed to pick up values from database
        	g.db = connect_db()
        	print fmobile
        	results = g.db.execute('Select * from subscriber where mobile=%s'%fmobile)
        	results = results.fetchall() # will give a list of tuples eg . [(1,2,3,4)]
        	print results # if mobile not in database then results will be []
        	if results != []:
        		data_dict = [dict(mobile=data[0],otp=data[1],name=data[2],email=data[3]) for data in results] #to cast the list into dictionary
        	# Now we will get a list of dictionary [{"mobile":"","otp":"","name":"","email":""}]
	    		if data_dict[0]['otp'] == fotp:
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
	    	        flash('Invalid credentials. Please try again.')
		        return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard(): #Later you would want to show the data for which user has logged in.
    # dummy data (created another table in database)
    g.db = connect_db()
    results = g.db.execute("Select * from posts")
    results = results.fetchall()
    print results
    data = [dict(name=result[0],comment=result[1]) for result in results]
    print data
    return render_template('dashboard.html',data=data) # passing data from database to dashboard.

@app.route('/logout') # Whenever someone hits the logout button
def logout():
	session.pop('loggedin',None) # Remove the session key on logout
	flash('You have been logged out')
        return redirect('/login')

if __name__ == '__main__':
	app.run(debug=True)

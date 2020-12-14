#------------------------ I M P O R T S -------------------------------
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#	initialize flask:
app = Flask(__name__)

#----------------------- D A T A B A S E ------------------------------
# situate database location:
#	3 slashes is relative path, 4 is absolute 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#	init db
db = SQLAlchemy(app)

#	create database model:
class Todo(db.Model):
	# int column for id, this is our primary key
	id = db.Column(db.Integer, primary_key=True)
	# content column, string, 200 char limit, not null
	content = db.Column(db.String(200), nullable=False)
	# autogenerate timestamp for data being written:
	date_created = db.Column(db.DateTime,
							 default=datetime.utcnow)
	
	def __repr__(self):
		return '<Task %r>' % self.id
"""
# after this point, return to a terminal, activate python3. from app
import db, and run 'db.create_all()' to create the database"""
#------------------------------ A P P --------------------------------
#	create index route:
"""
	supply the '@app.route()' decorator to the displaying function,
	passing in the endpoint as a string with a '/'. in front of it.  
	
	basic example:
	
	@app.route('/') #this defaults to "localhost/"
	def index():
		return "Hello, World!"
		
	we will utilize flask's render template function to display full
	webpages.
"""

@app.route('/', methods = ['POST', 'GET']) # accept these methods
def index():
	# if we're getting a POST method request:
	if request.method == 'POST':
		# the data collected from the form (id=content) in index.html
		task_content = request.form['content']
		# format task_content to fit db model:
		new_task = Todo(content=task_content)
		
		# try pushing new_task into db, or return error message:
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect("/") # go back to index.html
		except:
			return "There was an issue addin your task."
		
	else:
		# return all tasks in db in order of creation:
		tasks = Todo.query.order_by(Todo.date_created).all()
		# need to pass taks in here for jinja loop in index.html
		return render_template('index.html', tasks = tasks)

# route for deleting
"""
the <int:id> corresponds to the id on the task in the db.
delte entry with this id when you click the delete button of that
task.
"""
@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)
	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect("/")
	except:
		return "There was a problem with your delete request."
		
# route for updating
"""
the logic is to simply change the content of the entry with the
content on the update and return back to index.html
"""
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
	task_to_update = Todo.query.get_or_404(id)
	
	if request.method == 'POST':
		task_to_update.content = request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "There was a problem with your update request."
	else:
		return render_template('update.html', task = task_to_update)
		

#RUN
if __name__=="__main__":
	app.run(debug=True)

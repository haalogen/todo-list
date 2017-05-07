import sqlite3
from bottle import route, run, template, request
from bottle import debug


# Create An SQL Database
con = sqlite3.connect('todo.db')
con.execute("""CREATE TABLE IF NOT EXISTS todo (
	id INTEGER PRIMARY KEY,
	task char(100) NOT NULL,
	status bool NOT NULL
)""")


# Shows current todo-list
@route('/')
@route('/todo')
def todo_list():
	# Connect to DB and select all undone tasks
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")

	result = c.fetchall()
	c.close()

	# return tasks list as a table made from template
	return template('make_table.tpl', rows=result)


# Adds new task to todo-list
@route('/new', method='GET')
def new_item():

	if request.GET.save: # we got data from html-form

		new = request.GET.task.strip()

		# Connect to DB and add a new undone task
		conn = sqlite3.connect('todo.db')
		c = conn.cursor()

		c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
		new_id = c.lastrowid

		conn.commit()
		c.close()

		return '<p>The new task was inserted into the database, \
			the ID is %s</p>' % new_id
	else: # we need to send the html of form
		return template('new_task.tpl')


# Edits existing tasks
@route('/edit/<no:int>', method='GET')
def edit_item(no):
	if request.GET.save: # we got edited data
		edit = request.GET.task.strip()
		status = request.GET.status.strip()

		if status == 'open': # task is undone (open)
			status = 1
		else:
			status = 0

		# update task data in DB
		conn = sqlite3.connect('todo.db')
		c = conn.cursor()
		c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?",
							(edit, status, no))
		conn.commit()

		return '<p>The item number %s was successfully updated</p>' % no

	else: # We need to send html for user to edit task
		# Take the task's data from DB
		conn = sqlite3.connect('todo.db')
		c = conn.cursor()
		c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
		cur_data = c.fetchone()

		# return template for editing with task's data to user (frontend)
		return template('edit_task.tpl', old=cur_data, no=no)





debug(True) # shows a full stacktrace of the Python interpreter
# 'reloader' watches for web-server script change
run(port=8081, reloader=True)
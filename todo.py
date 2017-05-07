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

# Filling table for testing
# con.execute("INSERT INTO todo (task,status) VALUES \
# 	('Read A-byte-of-python to get a good introduction into Python',1)")
# con.execute("INSERT INTO todo (task,status) VALUES \
# 	('Visit the Python website',1)")
# con.execute("INSERT INTO todo (task,status) VALUES \
# 	('Test various editors for and check the syntax highlighting',1)")
# con.execute("INSERT INTO todo (task,status) VALUES \
# 	('Choose your favorite WSGI-Framework',1)")
# con.commit()


# Shows current todo-list
@route('/')
@route('/todo')
def todo_list():
	conn = sqlite3.connect('todo.db')
	c = conn.cursor()
	c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")

	result = c.fetchall()
	c.close()
	return template('make_table.tpl', rows=result)


# Adds new task to todo-list
@route('/new', method='GET')
def new_item():

	if request.GET.save:

		new = request.GET.task.strip()

		conn = sqlite3.connect('todo.db')
		c = conn.cursor()

		c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
		new_id = c.lastrowid

		conn.commit()
		c.close()

		return '<p>The new task was inserted into the database, \
			the ID is %s</p>' % new_id
	else:
		return template('new_task.tpl')


# Edits existing tasks
@route('/edit/<no:int>', method='GET')
def edit_item(no):
	if request.GET.save:
		edit = request.GET.task.strip()
		status = request.GET.status.strip()

		if status == 'open':
			status = 1
		else:
			status = 0

		conn = sqlite3.connect('todo.db')
		c = conn.cursor()
		c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?",
							(edit, status, no))
		conn.commit()

		return '<p>The item number %s was successfully updated</p>' % no

	else:
		conn = sqlite3.connect('todo.db')
		c = conn.cursor()
		c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
		cur_data = c.fetchone()

		return template('edit_task.tpl', old=cur_data, no=no)






debug(True) # shows a full stacktrace of the Python interpreter
run(port=8081, reloader=True)
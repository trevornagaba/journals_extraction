from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index')
def index():
	context = { 'field_names':["GL_ACCCOUNT", "JOURNAL_ID", "DESCRIPTION", "TRANSACTION DATE", "VALUE DATE", "AUTO_MANUAL", 
	"FSLI", "AMOUNT", "USER_ID"], 
				'previous_names':["GL_ACCCOUNT", "JOURNAL_ID", "DESCRIPTION", "TRANSACTION DATE", "VALUE DATE", "AUTO_MANUAL", 
	"FSLI", "AMOUNT", "USER_ID"],
				'file_names':["Master", "Chart of Accounts", "Mapped TB", "User List"] 
	}
	return render_template('index.html', name=index, data=context)
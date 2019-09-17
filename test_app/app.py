from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def hello():
	data = []
	return render_template("test.html", data = data)

@app.route('/test')
def test():
	dummy_file_names = ["Master", "Chart of Accounts", "Mapped TB", "User List"]
	return render_template('test.html', name=index, data=dummy_file_names)

if __name__ == '__main__':
 app.run(host="0.0.0.0", port=5000)
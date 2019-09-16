from flask import Flask, request, render_template
app = Flask(__name__)

import pandas as pd
import numpy as np
import os

@app.route('/other')
def base():

	dummy_data = { 'field_names':["GL_ACCCOUNT", "JOURNAL_ID", "DESCRIPTION", "TRANSACTION_DATE", "VALUE_DATE", "AUTO_MANUAL", 
	"FSLI", "AMOUNT", "USER_ID"], 
				'previous_names':["GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
	"FSLI", "TOTAL", "USER"],
				'file_names':["Master", "Chart of Accounts", "Mapped TB", "User List"],
				'master_fields' : ["N/A", "GL_ACCCOUNT", "JOURNAL_ID", "DESCRIPTION", "TRANSACTION DATE", "VALUE DATE", "AUTO_MANUAL", 
	"FSLI", "AMOUNT", "USER_ID"],
				'foreign_keys' : ["N/A", "GL_ACCCOUNT", "JOURNAL_ID", "DESCRIPTION", "TRANSACTION DATE", "VALUE DATE", "AUTO_MANUAL", 
	"FSLI", "AMOUNT", "USER_ID", "GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
	"FSLI", "TOTAL", "USER"]
	}
	return render_template('base.html', base=index, data=dummy_data)


@app.route('/')
def index():
	# Insert code to read file names
	dummy_file_names = ["Master", "Chart of Accounts", "Mapped TB", "User List"]
	return render_template('index.html', name=index, data=dummy_file_names)


@app.route('/select_files',methods = ['POST', 'GET'])
def select_files():
	if request.method == 'POST':
		data = request.form.to_dict() # This is a dictionary

		dummy_selected_files = { "GL_ACCOUNT" : "Master", "JOURNAL_ID": "Master", "USER_ID" : "User_List", "FSLI" : "Mapped_TB"}

		# Enter logic to seperately get field_names for each file

		dummy_field_names = { 
				"Master" : {"GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
							"FSLI", "TOTAL", "USER"}, 
				"Chart of Accounts" : {"GL_ACCOUNT", "FSLI", "BS/IS"}, 
				"Mapped_TB" : {"GL_ACCOUNT", "AMOUNT", "FSLI"},
				"User_List" : {"Username", "User_ID", "Role", "Department"}
				}


		dummy_data = { 'dummy_selected_files' : dummy_selected_files, 'dummy_field_names' : dummy_field_names }

		return render_template('map_name.html', name=select_files, data=dummy_data)


@app.route('/join_tables',methods = ['POST', 'GET'])
def join_tables():

	# Read field names in Master sheet

	dummy_master_fields = [ "GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
	"FSLI", "TOTAL", "USER", "N/A" ]
	
	# Read all fields except master
	# dummy_secondary_fields = { 
	# 					"Chart of Accounts" : {"GL_ACCOUNT", "FSLI", "BS/IS"}, 
	# 					"Mapped_TB" : {"GL_ACCOUNT", "AMOUNT", "FSLI"},
	# 					"User_List" : {"Username", "User_ID", "Role", "Department"},
	# 					"Other" : "N/A"
	# 				}

	dummy_secondary_fields = {"GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
						"FSLI", "TOTAL", "USER", "GL_ACCOUNT", "FSLI", "BS/IS", "GL_ACCOUNT", "AMOUNT", "FSLI"
			}

	if request.method == 'POST':
		mapping_data = request.form.to_dict()
		# for key, value in data.items():
		# 	if value not in dummy_master_fields:
		# 		secondary_fields.append(value)

		# 	print ("Unmatched fields: "+ str(secondary_fields))

		data = { 'dummy_master_fields': dummy_master_fields, 'dummy_secondary_fields':dummy_secondary_fields, 'mapping_data':mapping_data }

		return render_template('join_tables.html', name=join_tables, data=data)


@app.route('/transform',methods = ['POST', 'GET'])
def transform():
	if request.method == 'POST':
		data = request.form.to_dict()
		print(data)

		# Make joins as per primary secondary fields

		# Creating computed fields
		df['TRANSACTION DATE'] = pd.to_datetime(df['TRANSACTION DATE'])
		df['VALUE DATE'] = pd.to_datetime(df['VALUE DATE'])
		df['VALUE_DOW'], df['VALUE_MONTH'] = df['VALUE DATE'].dt.day, df['VALUE DATE'].dt.month
		df['TRANSACTION_DOW'], df['TRANSACTION_MONTH'] = df['TRANSACTION DATE'].dt.day, df['TRANSACTION DATE'].dt.month
		return GL_dump.to_excel("data/result/consolidated.xlsx")
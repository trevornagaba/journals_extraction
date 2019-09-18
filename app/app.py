from flask import Flask, request, render_template
app = Flask(__name__)

import pandas as pd
import numpy as np
import os
import xlrd

field_names = {}
secondary_field_names = []

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
	file_names = []
	file_extensions = []
	
	for f in os.listdir("../data/source/"):
	    file_extensions.append(f)
	    file_names.append(f.split(".")[0])
	print(file_names)
	return render_template('index.html', name=index, data=file_names)


@app.route('/select_files',methods = ['POST', 'GET'])
def select_files():
	if request.method == 'POST':
		selected_files = request.form.copy() # This is a dictionary
		print(selected_files)

		# dummy_selected_files = { "GL_ACCOUNT" : "Master", "JOURNAL_ID": "Master", "USER_ID" : "User_List", "FSLI" : "Mapped_TB"}

		file_names = []
		file_extensions = []
		
		for f in os.listdir("../data/source/"):
		    file_extensions.append(f)
		    file_names.append(f.split(".")[0])

		file_counter = 0
		
		for file in file_names:
			column_names = []
			wb = xlrd.open_workbook("../data/source/"+file_extensions[file_counter])
			print("type: "+str(wb))
			sheet = wb.sheet_by_index(0)
			# For row 0 and column 0
			sheet.cell_value(0, 0)
			file_counter=file_counter+1
			for i in range(sheet.ncols): 
			    print(sheet.cell_value(0, i)) 
			    column_names.append(sheet.cell_value(0, i))
			    secondary_field_names.append(sheet.cell_value(0, i))
			field_names[file] = column_names
			print(field_names)


		dummy_field_names = { 
				"Master" : {"GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
							"FSLI", "TOTAL", "USER"}, 
				"Chart of Accounts" : {"GL_ACCOUNT", "FSLI", "BS/IS"}, 
				"Mapped_TB" : {"GL_ACCOUNT", "AMOUNT", "FSLI"},
				"User_List" : {"Username", "User_ID", "Role", "Department"}
				}

		# master_field_names = field_names['master']
		print("here")
		print(field_names['master'])

		dummy_data = { 'selected_files' : selected_files, 'field_names' : field_names }

		return render_template('map_name.html', name=select_files, data=dummy_data)


@app.route('/join_tables',methods = ['POST', 'GET'])
def join_tables():
	dummy_master_fields = [ "GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
	"FSLI", "TOTAL", "USER", "N/A" ]
	dummy_secondary_fields = {"GL", "JOURNAL_NUMBER", "NARRATIVE", "POSTING DATE", "EFFECTIVE DATE", "AUTO_MANUAL", 
						"FSLI", "TOTAL", "USER", "GL_ACCOUNT", "FSLI", "BS/IS", "GL_ACCOUNT", "AMOUNT", "FSLI"
			}

	if request.method == 'POST':
		mapping_data = request.form.copy()
		print("mapped_data")
		print(mapping_data)
		field_names['master'].append('N/A')
		secondary_field_names.append('N/A')

		for field in field_names['master']:
			print(field)
			field.replace(" ", "_")
		for field in secondary_field_names:
			field.replace(" ", "_")
		print("After replace")
		print(field_names['master'])
		print(secondary_field_names)

		data = { 'master_field_names': field_names['master'], 'secondary_field_names': secondary_field_names, 'mapping_data':mapping_data }

		return render_template('join_tables.html', name=join_tables, data=data)


@app.route('/transform',methods = ['POST', 'GET'])
def transform():
	if request.method == 'POST':
		data = request.form.copy()
		print(data)

		for key, value in data.items():
			value.replace("_", " ")
		print("After re replace")
		print(data)

		for key, value in data.items():
			if value != "N/A":
				data.remove(key) # how to remove a value from a dictionary

		for file in selected_files:


		# Make joins as per primary secondary fields

		# Creating computed fields
		df = pd.read_excel("../data/source/master.xlsx")

		df.rename(columns=dictionary)


		df['TRANSACTION DATE'] = pd.to_datetime(df['TRANSACTION DATE'])
		df['VALUE DATE'] = pd.to_datetime(df['VALUE DATE'])
		df['VALUE_DOW'], df['VALUE_MONTH'] = df['VALUE DATE'].dt.day, df['VALUE DATE'].dt.month
		df['TRANSACTION_DOW'], df['TRANSACTION_MONTH'] = df['TRANSACTION DATE'].dt.day, df['TRANSACTION DATE'].dt.month
		return df.to_excel("data/result/consolidated.xlsx")
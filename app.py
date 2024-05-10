

from flask import Flask, render_template, request, redirect, jsonify, Response
import os
import json
import csv

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
def home():
   return render_template('index.html')

   
@app.route('/convertcsv', methods=["POST"])
def convert():
  # Checks if there is a file in the reqeest
  if 'file' not in request.files:
     # Sends error if no file is found
     return jsonify({'error' : 'No file part'})
  file = request.files['file']
  # Checks if there is a selected file
  if file.filename == '':
     return jsonify({'error':'No selected file'})
  if file:
     # Sets the path of the uploaded file
     file_path='./tmp/uploaded_file.csv'
     # Saves the uploaded file to the file path
     file.save(file_path)
     
     json_data =convert_csv_to_json(file_path)
     
     #Takes the list from convert_csv_to_json and converts it to a jsonfile
     return jsonify(json_data)
 
def convert_csv_to_json(file_path):
   # Empty list to store the converted CSV dATA
   json_data = []
   
   # Opens the file in read mode annd closes the file after the code is doen
   with open(file_path, 'r') as csv_file:
      # Creates a CSV reader object and creates a dictionary for each row with headers as keys and row values as values
      csv_reader = csv.DictReader(csv_file)
      #Iterates over each row in the dictionary
      for row in csv_reader:
         # Adds each row to the json_data list
         json_data.append(row)
   return json_data

@app.route('/convertjson', methods=["POST"])
def convertjson():
   # Gets the file from the request
   file = request.files['jsonfile']
   if file:
    # Saves the file in tmp folder
    file.save('./tmp/' + file.filename)
    #Opens the file
    with open('./tmp/' + file.filename) as f:
       #Dezerialise the json data from the file
       json_data = json.load(f)
   # Gets the keys of the json data
   headers = json_data[0].keys()
   # Opens data1.csv in writemode
   with open('data1.csv', 'w', newline='') as csv_file:
      # Creates a object capable of writing dicitonaris into CSV 
      writer = csv.DictWriter(csv_file, fieldnames=headers)
      # Writes the header row to the CSV file based on fieldnames from the dictwriter
      writer.writeheader()
      #Goes throug every row in json_data and writes it to the CSV file
      for row in json_data:
        writer.writerow(row)
   #Opens the file in read mode and reads the content into csv_data
   with open('data1.csv', 'r') as csv_file:
      csv_data = csv_file.read()
   # Returns the csv_file and specifies that it contains CSV data
   return Response(
      csv_data,
      mimetype='text/csv',
     headers={"Content-Disposition": "inline;filename=data1.csv"}
       )
if __name__ == '__main__':
   # Run the app server on localhost:4449
   app.run('localhost', 4449)
   
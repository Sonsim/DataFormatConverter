

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
  if 'file' not in request.files:
     return jsonify({'error' : 'No file part'})
  file = request.files['file']
  
  if file.filename == '':
     return jsonify({'error':'No selected file'})
  if file:
     file_path='./tmp/uploaded_file.csv'
     file.save(file_path)
     
     json_data =convert_csv_to_json(file_path)
     
     return jsonify(json_data)
 
def convert_csv_to_json(file_path):
   json_data = []
   
   with open(file_path, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for row in csv_reader:
         json_data.append(row)
   return json_data

@app.route('/convertjson', methods=["POST"])
def convertjson():
   file = request.files['jsonfile']
   if file:
    file.save('./tmp/' + file.filename)
    
    with open('./tmp/' + file.filename) as f:
       json_data = json.load(f)
   headers = json_data[0].keys()
   with open('data1.csv', 'w', newline='') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=headers)
      writer.writeheader()
      for row in json_data:
        writer.writerow(row)
   with open('data1.csv', 'r') as csv_file:
      csv_data = csv_file.read()
   return Response(
      csv_data,
      mimetype='text/csv',
      headers={"Content-disposition":
               "attachment;filename=data1.csv"}
       )
if __name__ == '__main__':
   # Run the app server on localhost:4449
   app.run('localhost', 4449)
   
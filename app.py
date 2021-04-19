# Required Imports
import os
from flask import Flask, request, jsonify
from MCQGenerator import MCQGenerator
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
course = db.collection('Courses')

@app.route('/api/<string:id>', methods=['GET'])
def generate_quiz(id):
    doc = course.document(id)
    module = doc.collection('Module').stream()
    content = ''
    for doc1 in module:
        doc1.to_dict()
        soup = BeautifulSoup(doc1.get('content'),"html.parser")
        content += "".join([p.text for p in soup.find_all("p")])
    questions = MCQGenerator(content,2)
    qu = questions.generate()
    return jsonify(qu), 200
  


if __name__ == "__main__":
    app.run(debug=True)
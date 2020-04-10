import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'book_review'
app.config["MONGO_URI"] = 'mongodb+srv://benm4ckenzie:Istanbul5x@myfirstcluster-beoum.mongodb.net/book_review?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_library')
def get_library():
    return render_template('library.html', book=mongo.db.book.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
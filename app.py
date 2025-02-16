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
    return render_template('library.html', book=mongo.db.book.find().sort("book_title"))



@app.route('/my_library')
def my_library():
    return render_template('mylibrary.html', reader=mongo.db.reader.find().sort("book_title")) 


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/mylibrary')
def mylibrary():
    return render_template('mylibrary.html', reader=mongo.db.reader.find())


@app.route('/contact_page')
def contact_page():
    return render_template('contact.html')


@app.route('/receipt')
def receipt():
    return render_template('receipt.html')


@app.route('/about_page')
def about_page():
    return render_template('about.html')


@app.route('/read_book/<reader_id>', methods=['GET'])
def read_book(reader_id):
    mongo.db.reader.update_one({"_id": ObjectId(reader_id)}, {"$set": {"read_book": True }})
    return redirect(url_for('mylibrary'))


@app.route('/to_read_book/<reader_id>', methods=['GET'])
def to_read_book(reader_id):
    mongo.db.reader.update_one({"_id": ObjectId(reader_id)}, {"$set": {"read_book": False }})
    return redirect(url_for('mylibrary'))


@app.route('/add_book')
def add_book():
    return render_template('addbook.html',
        title=mongo.db.title.find(),
        author=mongo.db.author.find(),
        genre=mongo.db.genre.find(),
        publisher=mongo.db.publisher.find())


@app.route('/submit_book', methods=['POST'])
def submit_book():
    author_name = request.form.get('author_name')
    author = mongo.db.author.find_one({"author_name": author_name})
    if author is None:
        mongo.db.author.insert_one({'author_name': author_name})
    book_title = request.form.get('book_title')
    title = mongo.db.title.find_one({"book_title": book_title})
    if title is None:
        mongo.db.title.insert_one({'book_title': book_title})
    genre_name = request.form.get('genre_name')
    genre = mongo.db.genre.find_one({"genre_name": genre_name})
    if genre is None:
        mongo.db.genre.insert_one({'genre_name': genre_name})
    publisher_name = request.form.get('publisher_name')
    publisher = mongo.db.publisher.find_one({"publisher_name": publisher_name})
    if publisher is None:
        mongo.db.publisher.insert_one({'publisher_name': publisher_name})
    book = mongo.db.book
    book.insert_one(request.form.to_dict())
    return redirect(url_for('get_library'))


@app.route('/add_to_mylibrary/<book_id>', methods=['GET'])
def add_to_mylibrary(book_id):
    user = mongo.db.reader
    my_book = mongo.db.book.find_one({"_id": ObjectId(book_id)})
    del my_book["_id"]
    user.insert_one(my_book)
    return redirect(url_for('mylibrary'))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.book.find_one({"_id": ObjectId(book_id)})
    return render_template('editbook.html', book=the_book)
      

@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    book = mongo.db.book
    book.update({'_id': ObjectId(book_id)},
    {
        'genre_name':request.form.get('genre_name'),
        'author_name':request.form.get('author_name'),
        'book_title': request.form.get('book_title'),
        'publisher_name': request.form.get('publisher_name'),
        'release_date':request.form.get('release_date'),
        'book_length':request.form.get('book_length'),
        'isbn_13':request.form.get('isbn_13'),
        'book_image':request.form.get('book_image'),
        'book_url':request.form.get('book_url')   
    })
    return redirect(url_for('get_library'))


@app.route('/delete_book/<reader_id>')
def delete_book(reader_id):
    mongo.db.reader.remove({'_id': ObjectId(reader_id)})
    return redirect(url_for('mylibrary'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)


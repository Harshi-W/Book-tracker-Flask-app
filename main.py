from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db = SQLAlchemy()
db.init_app(app)


class Book(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    author = Column(String(250), nullable=False)
    rating = Column(Float, nullable=False)



@app.route('/')
def home():
    ##READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_books = result.scalars()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        #UPDATE RECORD

        book_to_update = db.get_or_404(Book, id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_selected = db.get_or_404(Book, id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

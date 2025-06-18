from pymongo import MongoClient

# Connect to MongoDB Atlas (replace connection string with your own)
client = MongoClient('mongodb+srv://nduatihump:zOqKwMyCiuOXjX4K@cluster0.wcyfmwi.mongodb.net/')
db = client.bookstore
books = db.books

# Insert sample books
sample_books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 1299},
    {"title": "1984", "author": "George Orwell", "price": 999},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 1499},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "price": 899},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 1599}
]
books.insert_many(sample_books)

# CRUD Operations --

# READ: Find books with price > 10
expensive_books = books.find({"price": {"$gt": 1000}})
for book in expensive_books:
    print(book)

# UPDATE: Change price of a book (1984 to 1099)
books.update_one(
    {"title": "1984"},
    {"$set": {"price": 10.99}}
)

# DELETE: Remove a book (Pride and Prejudice)
books.delete_one({"title": "Pride and Prejudice"})
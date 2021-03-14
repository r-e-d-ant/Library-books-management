
from datetime import datetime
from book_manage import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))



# This class to hold Admins who uploads books.
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # create relationship with Uploaded Table.
    posts = db.relationship('Uploaded', backref='auth', lazy=True)
    
    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"
    
# This is a table where books gonna be saved.
class Uploaded(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(10))
    description = db.Column(db.Text)
    
    # Here db.ForeignKey('user.id'), mean that he have a relationship to our user model.
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __repr__(self):
        return f"Uploaded('{self.title}', '{self.author}', '{self.description}')"
    
# This is a table where all the borrowed books info 
# gonna be saved.
class Borrowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(10))
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Borrowed('{self.customer}', '{self.title}', '{self.author}', '{self.borrow_date}', '{self.return_date}')"


# This is a table to save users who borrow the book.
# And information of that book.
class Returned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(16), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    book_title = db.Column(db.String(100), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    borrowed_date = db.Column(db.DateTime, nullable=False)
    returned_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Returned('{self.customer_name}', '{self.book_title}', '{self.borrowed_date}', '{self.returned_date}')"

    

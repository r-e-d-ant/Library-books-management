

from datetime import datetime

from book_manage import app, db, bcrypt

from book_manage.forms import Upload, Borrow, LoginForm, RegistrationForm
from book_manage.models import Admin, Uploaded, Borrowed, Returned

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    books = Uploaded.query.order_by(Uploaded.id.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', title='Library-books-management', books=books)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        searched_book = request.form['searched_book']
        formatted_search = "%{}%".format(searched_book)
        books = Uploaded.query.filter(Uploaded.title.like(formatted_search)).all()
        return render_template('search.html', title='Library-books-management', books=books, searched_book=searched_book)
    else:
        page = request.args.get('page', 1, type=int)
        books = Uploaded.query.order_by(Uploaded.id.desc()).paginate(page=page, per_page=4)
        return render_template('home.html', title='Library-books-management', books=books)

@app.route('/user/<string:admin>')
@login_required
def admin_books(admin):
    page = request.args.get('page', 1, type=int)
    admin= Admin.query.filter_by(username=admin).first_or_404()
    books = Uploaded.query.filter_by(auth=admin)\
        .order_by(Uploaded.id.desc())\
        .paginate(page=page, per_page=4)
        
    return render_template('admin_books.html', title='Library-books-management', admin=admin, books=books)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book(book_id):
    one_book = Uploaded.query.get(book_id)
    return render_template("book.html", one_book=one_book, title=one_book.title)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = Upload()
    if form.validate_on_submit():
        book = Uploaded(title=form.title.data, author=form.author.data, description=form.description.data, auth=current_user)
        
        db.session.add(book)
        db.session.commit()
        flash('The book have been uploaded successfuly', 'success')
        return redirect(url_for('home'))
    
    return render_template('upload.html', title='Upload', form=form)


@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow(book_id):
    form = Borrow()
    books = Uploaded.query.get(book_id)
    
    #form.borrow_date.data = datetime.utcnow
    #borroweds = Borrowed.query.all()
    if form.validate_on_submit():
        borrow = Borrowed(customer=form.customer.data, title=form.title.data, author=form.author.data, borrow_date=form.borrow_date.data, return_date=form.return_date.data)
        
        db.session.add(borrow)
        db.session.commit()
        flash('Book borrowed successfully', 'success')
        return redirect(url_for('borrow_info'))
    
    elif request.method == 'GET':
        form.title.data = books.title
        form.author.data = books.author
        
    return render_template('borrow.html', title='Borrow', form=form, books=books)
    
@app.route('/borrow_edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow_edit(book_id):
    form = Borrow()
    borroweds = Borrowed.query.get(book_id)
    
    #form.borrow_date.data = datetime.utcnow
    #borroweds = Borrowed.query.all()
    if form.validate_on_submit():
        borroweds.customer = form.customer.data
        borroweds.title = form.title.data
        borroweds.author = form.author.data
        borroweds.borrow_date = form.borrow_date.data
        borroweds.return_date = form.return_date.data

        db.session.commit()
        flash('Borrowed info successfully changed', 'success')
        return redirect(url_for('borrow_info'))
    
    elif request.method == 'GET':
        form.customer.data = borroweds.customer
        form.title.data = borroweds.title
        form.author.data = borroweds.author
        form.borrow_date.data = borroweds.borrow_date
        form.return_date.data = borroweds.return_date
    
        
    
    return render_template('borrow.html', title='Borrowed Edit', form=form, borroweds=borroweds)

@app.route('/borrow_info')
@login_required
def borrow_info():
    borrow_infos = Borrowed.query.all()
    
    return render_template('borrow_info.html', title='Borrow-Info', borrow_infos=borrow_infos)

@app.route('/borrow_info/<int:borrow_info_id>/delete_borrow_info', methods=['GET', 'POST'])
@login_required
def delete_borrow_info(borrow_info_id):
    borroweds = Borrowed.query.get(borrow_info_id)
    db.session.delete(borroweds)
    db.session.commit()

    flash('Your book borrow info have been deleted!', 'success')
    return redirect(url_for('borrow_info'))

@app.route('/return/<int:book_id>')
@login_required
def return_book(book_id):
    returns = Returned.query.get(book_id)
    borrow_infos = Borrowed.query.get(book_id)
    if returns == borrow_infos:
        pass
    else:
        add_to_returned = Returned(customer_name=borrow_infos.customer, customer_id=borrow_infos.id, book_title=borrow_infos.title, book_author=borrow_infos.author, borrowed_date=borrow_infos.borrow_date, returned_date=borrow_infos.return_date)
        db.session.add(add_to_returned)
        db.session.delete(borrow_infos)
        db.session.commit()
        flash('Book returned successfully and added into returned book history', 'success')
            
        return redirect(url_for('borrow_info'))
    
@app.route('/return_info')
@login_required
def return_info():
    return_infos = Returned.query.all()
    
    return render_template('return_info.html', title='Return Info', return_infos=return_infos)


@app.route('/return_info/<int:return_info_id>/delete_return_info', methods=['GET', 'POST'])
@login_required
def delete_return_info(return_info_id):
    returns = Returned.query.get(return_info_id)
    db.session.delete(returns)
    db.session.commit()

    flash('Your book return info have been deleted!', 'success')
    return redirect(url_for('return_info'))
            

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash(f"Your Account has been created! You are now able to login.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
    
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
        
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home/<int:book_id>/update', methods=['GET', 'POST'])
@login_required
def update(book_id):
    form = Upload()
    books = Uploaded.query.get(book_id)

    if form.validate_on_submit():
        books.title = form.title.data
        books.author = form.author.data
        books.description = form.description.data
        db.session.commit()
        flash('Your book have been updated!', 'success')
        
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        form.title.data = books.title
        form.author.data = books.author
        form.description.data = books.description
        
    return render_template('update.html', title='Update', form=form, books=books)

@app.route('/home/<int:book_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(book_id):
    book = Uploaded.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    flash('Your book have been deleted!', 'success')
    return redirect(url_for('home'))

    


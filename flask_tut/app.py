from flask import Flask , render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/libmng'#/dbname
app.secret_key = 'abc'
db = SQLAlchemy(app)

class Signup(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    usn = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(8), unique=False, nullable=False)
class Book(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    book_author = db.Column(db.String(50), primary_key=True)
    book_name = db.Column(db.String(50), unique=False, nullable=False)
    book_qty = db.Column(db.Integer, unique=False, nullable=False)
class Issuebook(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    usn = db.Column(db.String(50), primary_key=True)
    book_name = db.Column(db.String(50), unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    issue_date = db.Column(db.Date, unique=False, nullable=False)
    return_date = db.Column(db.Date, unique=False, nullable=False)
class Feedback(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False) 
    feedback = db.Column(db.String(100), unique=False, nullable=False)
class Fine(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False) 
    bookname = db.Column(db.String(50), unique=False, nullable=False) 
    fine = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.String(50))
    issuedate = db.Column(db.Date, unique=False, nullable=False)
    returndate = db.Column(db.Date, unique=False, nullable=False)


@app.route('/', methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        email=request.form.get('email')
        usn=request.form.get('usn')
        name=request.form.get('name')
        password=request.form.get('psw')
       
        entry= Signup(email=email,usn=usn,name=name,password=password)
        db.session.add(entry)
        db.session.commit()
        return render_template("success.html")
    return render_template("signup.html")    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method=='POST'):
        y=0
        email=request.form.get('email')
        password=request.form.get('psw')
        admin = 'admin123'
        admin_password = 'admin123'
        if(email==admin and password==admin_password):
            return redirect(url_for('admin'))

        #tablename
        
        Check = Signup.query.all()
        for x in Check:
            if(email==x.email and password==x.password):
                session['name'] = x.name
                session['usn'] = x.usn
                y=1
                return redirect(url_for('index'))
        if y==0:
            return render_template('error.html')    
         
    return render_template('login.html')

@app.route('/index',methods = ['GET','POST'])
def index():     
    name = session['name']
    book = Book.query.order_by(Book.sn.asc())
    return render_template('index.html', em1 = name, book = book)
@app.route('/admin')
def admin():
     data = Signup.query.all()
     return render_template('admin.html', students = data)
      
@app.route('/edit/<string:sn>', methods = ['GET','POST'])
def edit(sn):
    if(request.method=='POST'):
        email = request.form.get('email')
        usn = request.form.get('usn')
        name = request.form.get('name')
        
        student = Signup.query.filter_by(sn=sn).first()
        student.email = email
        student.usn = usn
        student.name = name
        
        db.session.commit()
        return redirect('/admin')
    student = Signup.query.filter_by(sn=sn).first()
    return render_template('edit.html',student=student)  
@app.route('/delete/<string:sn>', methods = ['GET','POST'])
def delete(sn):
    student = Signup.query.filter_by(sn=sn).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/admin')    
@app.route('/book', methods = ['GET','POST'])
def book():
    data = Book.query.order_by(Book.sn.asc())
    return render_template('book.html', book = data)
        
@app.route('/addbook', methods = ['GET','POST'])
def addbook():
        if(request.method=='POST'):
            book_id= request.form.get('book_id')
            book_author= request.form.get('book_author')
            book_name= request.form.get('book_name')
            book_qty= request.form.get('book_qty')
            entry= Book(book_id=book_id,book_author=book_author,book_name=book_name,book_qty=book_qty)
            db.session.add(entry)
            db.session.commit()
            return redirect('/book')
        return render_template('addbook.html')
@app.route('/editbook/<string:sn>', methods = ['GET','POST'])
def editbook(sn):
        if(request.method=='POST'):
            book_id= request.form.get('book_id')
            book_author= request.form.get('book_author')
            book_name= request.form.get('book_name')
            book_qty= request.form.get('book_qty')
            book = Book.query.filter_by(sn=sn).first()
            book.book_id = book_id
            book.book_author = book_author
            book.book_name = book_name
            book.book_qty = book_qty
            db.session.commit()
            return redirect('/book')
        book = Book.query.filter_by(sn=sn).first()
        return render_template('bookedit.html',book=book)
@app.route('/deletebook/<string:sn>', methods = ['GET','POST'])
def deletebook(sn):
    book = Book.query.filter_by(sn=sn).first()
    y=0
    issuebook = Issuebook.query.all()
    for x in issuebook:
        if(x.book_id==book.book_id and x.book_name==book.book_name):
         y=1
    if y==1:
        return render_template('error3.html')
    else:
        db.session.delete(book)
        db.session.commit()
        
    
    return redirect('/book')         
@app.route('/issuebook/<string:book_id>', methods = ['GET','POST'])
def issuebook(book_id):
    name = session['name']
    usn = session['usn']
    y=0
    book = Book.query.filter_by(book_id=book_id).first()
    book_name = book.book_name
    book_id = book.book_id
    
    issue_date = (date.today())
    return_date = (date.today()+timedelta(days=10))
    issuebook = Issuebook.query.all()
    for x in issuebook:
        if(x.book_id == book_id and x.usn==usn and x.book_name == book_name and x.name == name):
            y=1
    session['issue_date']=issue_date
    session['return_date']=return_date
    if y == 1:
        return render_template('error2.html')
    else:
        if(book.book_qty==0):
            return render_template('error4.html')
        book.book_qty = book.book_qty -1
        
        db.session.commit()
        entry= Issuebook(book_id=book_id,usn=usn,book_name=book_name,name=name,issue_date=issue_date,return_date=return_date)
        db.session.add(entry)
        db.session.commit()

    
    return render_template('issue.html', em1=name,em2=usn,book_name=book_name,book_id=book_id,issue_date=issue_date,return_date=return_date)
@app.route('/mybook')
def mybook():
    usn = session['usn']
    issuebook = Issuebook.query.filter_by(usn=usn)
    return render_template('mybook.html',issuebook=issuebook)       
@app.route('/issuedbook')
def issuedbook():
    issuebook = Issuebook.query.all()
    return render_template('issuedbook.html',issuebook=issuebook)     
@app.route('/returnbook/<string:sn>', methods = ['GET','POST'])
def returnbook(sn):
    book = Issuebook.query.filter_by(sn=sn).first()
    date1 = (date.today())
    session['usn']=book.usn
    return_date = book.return_date
    name = book.name
    book_name = book.book_name
    usn = book.usn
    issue_date = book.issue_date
    #born = datetime.date(2021, 1, 15)
    delta = date1 - return_date
    if(delta.days<=0):
        fine=0
    else:
        fine = delta.days * 5
    
        
    status = 'Unpaid'        
    entry = Fine(usn=usn,name=name,bookname=book_name,fine=fine,status=status,issuedate=issue_date,returndate=date1)
    db.session.add(entry)
    db.session.commit()      
    return redirect('/fine')   
@app.route('/fine', methods = ['GET','POST'])
def fine():
    usn = session['usn']
    fine = Fine.query.filter_by(usn=usn)
    return render_template("fine.html",fine=fine)

@app.route('/paid/<string:sn>', methods = ['GET','POST'])
def paid(sn):
    fine = Fine.query.filter_by(sn=sn).first()
    book = Issuebook.query.all()
    for data in book:
        if( data.usn == fine.usn and data.issue_date == fine.issuedate and data.book_name == fine.bookname):
            status = 'paid'
            fine.status = status
            db.session.commit()
            sn=data.sn
    book1 = Issuebook.query.filter_by(sn=sn).first()
    book1_name = book1.book_id
    book1_bookname = book1.book_name
    y = 0
    db.session.delete(book1)
    db.session.commit()
    book2 = Book.query.all()
    for x in book2:
        if(x.book_id == book1_name and x.book_name == book1_bookname):
            sn2 = x.sn
            y = 1
    if y == 1:
         book3 = Book.query.filter_by(sn=sn2).first()       
         book3.book_qty = book3.book_qty + 1
         db.session.commit()
   

    return redirect('/issuedbook')

@app.route('/feedback', methods = ['GET','POST'])
def feedback():
    name = session['name']
    if(request.method=='POST'):
        feedback = request.form.get('feedback')
        name = session['name']
        entry= Feedback(name = name, feedback=feedback)
        db.session.add(entry)
        db.session.commit()
        return redirect('/index') 
    return render_template('feedback.html', name=name) 

@app.route('/feedbackdisplay', methods = ['GET','POST'])
def feedbackdisplay():
    feedback = Feedback.query.all()
    return render_template('feedbackdisplay.html', feedback=feedback)

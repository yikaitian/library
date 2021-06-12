import datetime
import time

from app import get_logger, get_config
from flask import render_template, redirect, url_for, flash
from app.main.book.forms import LoanForm, ReturnForm
from app.main.book.views import books_list, book_loans_list, borrower_list, book_loans_due_list, index_status
from app.models import Book, LibraryBranch, BookCopies, Borrower, BookLoans
from . import main

logger = get_logger(__name__)
cfg = get_config()


# 路由配置

# 用户页面
@main.route('/', methods=['GET', 'POST'])
def index():
    return books_list('users/list.html')

@main.route('/hello', methods=['GET', 'POST'])
def hello_index():
    return render_template('users/test.html')

# 管理员页面
@main.route('/admin', methods=['GET'])
def adminIndex():
    return books_list('admin/books/list.html')


# 图书列表
@main.route('/admin/book/list', methods=['GET', 'POST'])
def adminBookList():
    return books_list('admin/books/list.html')


# 借阅列表
@main.route('/admin/book/loans', methods=['GET', 'POST'])
def adminBookLoansList():
    return book_loans_list('admin/books/book_loans.html')


# 逾期列表
@main.route('/admin/book/loans_due', methods=['GET', 'POST'])
def adminBookLoansDueList():
    return book_loans_due_list('admin/books/book_loans.html')


# 借阅和归还
@main.route('/admin/book/manage', methods=['GET', 'POST'])
def adminBookManage():
    loan_form = LoanForm()
    return_form = ReturnForm()

    if loan_form.validate_on_submit():
        try:
            book = Book.select().where(Book.BookId == loan_form.BookId.data)
            if not book:
                flash(message="Can't find the book", category='warning')
                return redirect(url_for('main.adminBookManage'))

            branch = LibraryBranch.select().where(LibraryBranch.BranchId == loan_form.BranchId.data)
            if not branch:
                flash(message="Can't find book branch", category='warning')
                return redirect(url_for('main.adminBookManage'))
            book_copie = BookCopies.select().where(BookCopies.BookId == loan_form.BookId.data,
                                                   BookCopies.BranchId == loan_form.BranchId.data)
            if not book_copie:
                flash(message="The book is not in the book branch", category='warning')
                return redirect(url_for('main.adminBookManage'))

            borrower = Borrower.create(CardNo=time.time(), Name=loan_form.Name.data, Address=loan_form.Address.data,
                                       Phone=loan_form.Phone.data)
            borrower.save()

            book_loan = BookLoans.create(
                BookId=loan_form.BookId.data,
                BranchId=loan_form.BranchId.data,
                CardNo=borrower.CardNo,
                DateOut=datetime.datetime.now(),
                DueDate=datetime.datetime.now() + datetime.timedelta(days=loan_form.Date.data),
                returned=0
            )
            book_loan.save()
            flash(message='Successfully borrowed', category='success')
            return redirect(url_for('main.adminBookManage'))

        except Exception as e:
            print(e)
            flash(message='Submit parameter error', category='warning')
            return redirect(url_for('main.adminBookManage'))

    if return_form.validate_on_submit():
        try:
            book_loan = BookLoans.select().where(BookLoans.returned == 0, BookLoans.BookId == return_form.BookId.data)
            print(book_loan)
            if not book_loan:
                flash(message='No relevant borrowing information found', category='warning')
                return redirect(url_for('main.adminBookManage'))
            book_loan_item = book_loan.get()
            borrower = Borrower.select().where(Borrower.CardNo == book_loan_item.CardNo,
                                               Borrower.Name == return_form.Name.data)

            if not borrower:
                flash(message='User information not found', category='warning')
                return redirect(url_for('main.adminBookManage'))

            query = (BookLoans
                     .update(returned=1)
                     .where(BookLoans.returned == 0, BookLoans.BookId == return_form.BookId.data,
                            BookLoans.CardNo == book_loan_item.CardNo))
            query.execute()
            flash(message='Returned successfully', category='success')
            return redirect(url_for('main.adminBookManage'))

        except Exception as e:
            print(e)
            flash(message='Submit parameter error', category='warning')
            return redirect(url_for('main.adminBookManage'))

    return render_template('admin/books/manage.html', loan_form=loan_form, return_form=return_form)


# 借阅人列表
@main.route('/admin/book/borrower', methods=['GET', 'POST'])
def adminBorrower():
    return borrower_list('admin/books/borrower.html')

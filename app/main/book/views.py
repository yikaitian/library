import datetime

from peewee import JOIN

from app import get_logger, get_config
import math
from flask import render_template, request
from app import utils
from app.models import Book, LibraryBranch, BookCopies, BookLoans, Borrower, Author

logger = get_logger(__name__)
cfg = get_config()


def index_status(view):
    """
    首页信息
    :param view:
    :return:
    """
    book = Book.select()
    library_branch = LibraryBranch.select()
    borrower = Borrower.select()
    books_loan = BookLoans.select().where(BookLoans.returned == 0)

    data = {
        'books': book.count(),
        'branchs': library_branch.count(),
        'borrowers': borrower.count(),
        'loans': books_loan.count()
    }
    return render_template(view, data=data)


def books_list(view):
    """
    图书列表
    :param view:
    :return:
    """
    # 接收参数
    search = request.args.get('search')
    branch = request.args.get('branch')

    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE
    branch_data = LibraryBranch.select()

    branch_book_id = []
    if branch and branch != "0":
        query = BookCopies.select().where(BookCopies.BranchId == branch)
        for item in query:
            branch_book_id.append(item.BookId)

    # 查询列表
    if search:
        if branch_book_id:
            query = Book.select(Book.BookId, Book.Title, Book.PublisherName, Book.Author, Author.AuthorName,
                                BookLoans.DueDate).join(
                Author, on=(Book.Author == Author.AuthorId)).switch(Book).join(BookLoans, JOIN.LEFT_OUTER, on=(
                        (Book.BookId == BookLoans.BookId) & (branch == BookLoans.BranchId))).where(
                (Book.Title ** "%{s}%".format(s=search.strip()) |
                 Book.Author ** "%{s}%".format(s=search.strip())),
                Book.BookId.in_(branch_book_id), ((BookLoans.returned.is_null(True)) | (BookLoans.returned != 1)))
        else:
            query = Book.select(Book.BookId, Book.Title, Book.PublisherName, Book.Author, Author.AuthorName).join(
                Author, on=(Book.Author == Author.AuthorId)).orwhere(Book.Title ** "%{s}%".format(s=search.strip()),
                                                                     Book.Author ** "%{s}%".format(s=search.strip()))
    else:
        if branch_book_id:
            query = Book.select(Book.BookId, Book.Title, Book.PublisherName, Book.Author, Author.AuthorName,
                                BookLoans.DueDate).join(
                Author, on=(Book.Author == Author.AuthorId)).switch(Book).join(BookLoans, JOIN.LEFT_OUTER, on=(
                        (Book.BookId == BookLoans.BookId) & (branch == BookLoans.BranchId))).where(
                Book.BookId.in_(branch_book_id), ((BookLoans.returned.is_null(True)) | (BookLoans.returned != 1)))
        else:
            query = Book.select(Book.BookId, Book.Title, Book.PublisherName, Book.Author, Author.AuthorName).join(
                Author, on=(Book.Author == Author.AuthorId))

    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query.dicts()), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}

    return render_template(view, form=dict, branch=branch_data)


def book_loans_list(view):
    """
    图书借阅列表
    :param view:
    :return:
    """
    # 接收参数
    search = request.args.get('search')

    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 查询列表
    if search:
        borrower_list = []
        borrower_query = Borrower.select().where(Borrower.Name ** "%{s}%".format(s=search.strip()))
        for i in borrower_query:
            borrower_list.append(i.CardNo)

        query = BookLoans.select(BookLoans, Borrower, LibraryBranch, Book.Title).join(Borrower, on=(
                    BookLoans.CardNo == Borrower.CardNo)).switch(BookLoans).join(LibraryBranch, on=(
                    BookLoans.BranchId == LibraryBranch.BranchId)).switch(BookLoans).join(Book, on=(
                    BookLoans.BookId == Book.BookId)).where((BookLoans.BookId == search.strip()) | (BookLoans.CardNo.in_(borrower_list))).order_by(BookLoans.DateOut.desc())
    else:
        query = BookLoans.select(BookLoans, Borrower, LibraryBranch, Book.Title).join(Borrower, on=(
                    BookLoans.CardNo == Borrower.CardNo)).switch(BookLoans).join(LibraryBranch, on=(
                    BookLoans.BranchId == LibraryBranch.BranchId)).switch(BookLoans).join(Book, on=(
                    BookLoans.BookId == Book.BookId)).order_by(BookLoans.DateOut.desc())

    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query.dicts()), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict)


def book_loans_due_list(view):
    """
    借阅逾期列表
    :param view:
    :return:
    """
    # 接收参数
    search = request.args.get('search')

    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 查询列表
    if search:
        borrower_list = []
        borrower_query = Borrower.select().where(Borrower.Name ** "%{s}%".format(s=search.strip()))
        for i in borrower_query:
            borrower_list.append(i.CardNo)
        query = BookLoans.select(BookLoans, Borrower, LibraryBranch, Book.Title).join(Borrower, on=(
                    BookLoans.CardNo == Borrower.CardNo)).switch(BookLoans).join(LibraryBranch, on=(
                    BookLoans.BranchId == LibraryBranch.BranchId)).switch(BookLoans).join(Book, on=(
                    BookLoans.BookId == Book.BookId)).where(BookLoans.DueDate <= datetime.datetime.now(), ((BookLoans.BookId == search.strip()) | (BookLoans.CardNo.in_(borrower_list)))).order_by(BookLoans.DateOut.desc())
    else:
        query = BookLoans.select(BookLoans, Borrower, LibraryBranch, Book.Title).join(Borrower, on=(
                    BookLoans.CardNo == Borrower.CardNo)).switch(BookLoans).join(LibraryBranch, on=(
                    BookLoans.BranchId == LibraryBranch.BranchId)).switch(BookLoans).join(Book, on=(
                    BookLoans.BookId == Book.BookId)).where(BookLoans.DueDate <= datetime.datetime.now()).order_by(BookLoans.DateOut.desc())

    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query.dicts()), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict)


def borrower_list(view):
    """
    借阅人列表
    :param view:
    :return:
    """
    # 接收参数

    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    query = Borrower.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict)

p

## Introduction

library is a book management system developed based on the flask framework. It mainly contains two interfaces, one is the root interface, which can be used to query the status of books, and the other is the administrator interface, which can be accessed through /admin to view the status of books, manage the borrow or return of books and check the borrowing records, etc.

The library project has the following characteristics：

1. Use Flask as web framework and use Jinja template as default
2. Use Peewee as ORM framework, which can easily interacts with the database
3. The front-end application is based on BootStrap template so the interface is simple and practical

## Compatibility

- python3.8(recommend)
- peewee
- pymysql
- flask
- flask-script
- flask-wtf
- pymysql

## Python environment third-party dependency installation
```python
pip3 install -r requirements.txt
or pip install -r requirements.txt
```

## System parameter configuration and operation
1. Edit`config.py`, modify SECRET_KEY and MySQL database related parameters

   ```
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
   DB_HOST = '127.0.0.1'
   DB_USER = 'user'
   DB_PASSWD = 'password'
   DB_DATABASE = 'library'
   ```

2. Edit log-app.conf, modify the log path as needed

   ```
   args=('/path/to/log/flask-rest-sample.log','a','utf8')
   ```

3. mysql environment modify

   ```
   # run in mysql shell, replace the following path according to the project location (absolute path)
   source E：/library/sql_file/library.sql
   source E：/library/sql_file/libdata.sql
   ```

4. run

   ```
   python manage.py runserver
   ```

   and access[http://127.0.0.1:8000](http://127.0.0.1:8000/)

   If there is an error, please check according to the error message

## Project directory structure

- /app/main  Main function point related code
- /app/static  JS、CSS Static file
- /app/template  HTML template
- /app/models.py  Peewee models
- /app/utils.py  Tools module
- /conf  System parameters and log configuration
- /sql_file Databases file
- /env Virtual environment related documents


## Related learning documents
- [http://flask.pocoo.org](http://flask.pocoo.org)
- [https://flask-script.readthedocs.io](https://flask-script.readthedocs.io)
- [https://flask-wtf.readthedocs.io](https://flask-wtf.readthedocs.io)
- [http://docs.peewee-orm.com](http://docs.peewee-orm.com)
- [https://almsaeedstudio.com/preview](https://almsaeedstudio.com/preview)

## Specific introduction

### Project routing settings

library project mainly includes the following accessible addresses

/ Root address, user access interface, you can query the status of books

/admin Administrators can access the interface and can query the status of books

/admin/book/list Administrators can access the interface and can query the status of books

/admin/book/loans Administrator can accesses the interface and can query the book borrowing records

/admin/book/loans_due Administrator can visits the interface and can query overdue records of books

/admin/book/borrower Administrator can accesses the interface and can query the records of the book borrowers

/admin/book/manage Administrator can access interface, can manage book borrowing and return

Because the project routing situation is not complicated, only one blueprint main is registered in the flask framework, and blueprints can be added as needed in the future.

### Project models design

The library project mainly includes 7 models, which are designed according to the project requirements and call peewee (ORM library) to interact with the database.

author model, record the author name information

Publisher model, record the name, address, and telephone of the publisher

Book model, record book name, publisher, author information

library_branch model, record the name and address of the library

book_copies model, record the book id, library id, and whether the book is in the library

The borrower model records the user's name, address, and phone number

The book_loans model records the book id, library id, user id, borrowing date, and return date.

### Project templates design

The library mainly uses the styles and formats provided by bootstrap for template design, all interfaces are inherited from base.html

base.html uses bootstrap's grid system to design a rough model of all interfaces, mainly including the top title, the navigation bar on the left, and the main interface on the right.

For users, the title is library system, and there is only one navigation bar, which can only navigate to the root address. The main interface calls the view function to display the book information and can query at the same time

For administrators, the title is library system, there are only five navigation bars, and you can navigate to five administrator addresses, /admin/book/list, /admin/book/loans, /admin/book/loans_due, /admin/book/ The borrower, /admin/book/manage, and the corresponding operations can be performed on the main interface on the right.

### Project view function design

/Root address and /admin/book/list mainly use the view function book_list to render list.html. The book_list function first reads the form sent by the user (requests.args), and then uses peewee to view the database according to the search conditions Query query for the data, and finally render the table in the html template with the query result.

The other three addresses /admin/book/loans, /admin/book/loans_due, /admin/book/borrower also use the view functions book_loans_list, book_loans_due_list, and borrower_list to query the database, and use the query results to render the table in the html template

/admin/book/manage uses the view function adminBookManage to obtain the form, determine whether to borrow or return it, and then rewrite and add the corresponding database information according to the information.




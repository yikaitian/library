from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoanForm(FlaskForm):
    """
    借阅表单
    """
    BookId = StringField('BookId', validators=[DataRequired()])
    BranchId = StringField('BookId', validators=[DataRequired()])
    Name = StringField('Name', validators=[DataRequired()])
    Address = StringField('Address', validators=[DataRequired()])
    Phone = StringField('Phone', validators=[DataRequired()])
    Date = IntegerField('Date', validators=[DataRequired()], default=28)
    submit = SubmitField('submit')


class ReturnForm(FlaskForm):
    """
    归还表单
    """
    BookId = StringField('BookId', validators=[DataRequired()])
    Name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('submit')

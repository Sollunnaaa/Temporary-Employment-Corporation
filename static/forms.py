from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, SubmitField,IntegerField,FloatField,SelectField,HiddenField,BooleanField,PasswordField
from wtforms.validators import Length,DataRequired, EqualTo,ValidationError
from datetime import datetime

class OpeningForm(FlaskForm):
    JobName = StringField(label='Name:', validators=[Length(min=2,max=200), DataRequired()])
    pay = IntegerField(label='Price:',validators=[DataRequired()])
    description = StringField('Description')
    Startdate = DateField('Start Date: ', validators=[DataRequired()], default=datetime.today().date)
    Enddate = DateField('End Date: ', validators=[DataRequired()], default=datetime.today().date)
    jobshift = StringField('Description')
    jobtype = StringField('Description')
    address=StringField('Description')
    submit = SubmitField(label='Submit')

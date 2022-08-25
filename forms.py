from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class sign_up(FlaskForm):
    username=StringField('Enter The Email: ',validators=[DataRequired()])
    name=StringField("Enter Your Name",validators=[DataRequired()])
    password=PasswordField("Enter The Password")
    submit=SubmitField("Submit")

class login(FlaskForm):
    email=StringField("Enter The Email: ",validators=[DataRequired()])
    password=PasswordField("Enter The Password:  ",validators=[DataRequired()])
    submit=SubmitField("Submit")

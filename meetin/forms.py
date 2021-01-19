from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField,IntegerField,FloatField,SelectMultipleField,DateTimeField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Optional
from meetin.database import get_all_category,get_all_university

def choice(liste):
    result = list()
    
    for every in liste:
        keys = list(every)
    
        result.append((every[keys[0]],every[keys[1]]))
    return result
class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me',default = False)
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label=('Register'))

class UpdateProfileform(FlaskForm):
    
    bio = TextAreaField('Bio')
    university = SelectField(label = 'University',coerce = int)
    birthDate = DateTimeField(label = 'Birth Date',format='%d/%m/%Y',validators=[Optional()])
    photoUrl = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jfif','jpeg'], 'Images only')])
    urlInstagram = StringField('Instagram')
    urlTwitter = StringField('Twitter')
    urlFacebook = StringField('Facebook')
    occupation = StringField('Occupation')
    gender = RadioField('Gender', choices=[(1,'Male'),(2,'Female'),(3,'Other')],coerce = int)
    save = SubmitField(label = ('Save'))

class EventForm(FlaskForm):
    
    eventName = StringField('Event Name',validators=[DataRequired()])
    description = TextAreaField('Description',validators=[DataRequired()])
    category = SelectField(label = 'Category',coerce = int,validators=[DataRequired()])
    eventdate = DateTimeField(label = 'Event Date',format='%d/%m/%Y',validators=[DataRequired()] )
    eventPhotoUrl = FileField('Event Photo', validators=[FileAllowed(['jpg', 'png','jfif','jpeg'], 'Images only')])
    eventLink = StringField('Event Link')
    save = SubmitField(label = ('Save'))

class EnrollForm(FlaskForm):
    reason = StringField('Why are you attending', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SimpleForm(FlaskForm):
    field = StringField(validators=[DataRequired()])
    submit = SubmitField()



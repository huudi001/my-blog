from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class ComentForm(FlaskForm):

    title = StringField('Feedback title',validators=[Required()])
    comment = TextAreaField(' feedback', validators=[Required()])
    submit = SubmitField('Submit')


class ArticleForm(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    body= TextAreaField('Pitch body', validators=[Required()])
    submit = SubmitField('Submit')

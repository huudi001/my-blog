from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    comment_content =  TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')

class ArticleForm(FlaskForm):
    article_title = StringField('article Title')
    article_content = TextAreaField('article Content')
    submit = SubmitField('Submit')

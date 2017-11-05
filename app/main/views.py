from flask import render_template,redirect,url_for
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from . import main
from ..models import User
#from .forms import Form,FeedbackForm

@main.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title = title)
@main.route('/new/<int:id>', methods = ["GET", "POST"])
@login_required
def new_post(id):

    form = PostForm()
    if form.validate_on_submit():
        post_title = form.title.data
        post_body = form.body.data

        new_post = Post( post_title = title, post_body = body, user = current_user)
        db.session.add(new_post)
        return redirect(url_for('main.route'))
        title = {category.name}
    return render_template('new_post.html', title = title, post_form = form)

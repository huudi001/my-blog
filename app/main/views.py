from flask import render_template,redirect,url_for
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from . import main
from ..models import User
#from .forms import Form,FeedbackForm

@main.route('/')
def index():
    #user= User.query.all()
    title = 'Home'
    return render_template('index.html', title = title)

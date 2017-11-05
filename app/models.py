from . import db
from . import login_manager
from flask_login import UserMixin

from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(UserMixinuser_id):
    return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    pass_secure = db.Column(db.String(255))

    def __repr__(self):
        return  {self.username}


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return  {self.name}

class Post(db.Model):
    __table__name = 'posts'
    id = db.Column(db.Integer,primary_key = True)
    post_body = db.Column(db.String(255))
    post_title = db.Column(db.String(255))
    user_id= db.Column(db.Integer, db.ForeignKey("users.id") )

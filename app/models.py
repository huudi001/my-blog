from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, timezone
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

class Role(db.Model):

    __tablename__ = 'roles'


    id = db.Column(db.Integer, primary_key = True)


    name = db.Column(db.String)


    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'
class User(UserMixin,db.Model):


    __tablename__ = 'users'

    # id column that is the primary key
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index)
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    articles = db.relationship('Article', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    register = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'User {self.username}'

    @classmethod
    def check_role(cls,user_id,role_id):
        get_role = User.query.filter_by(id=user_id).filter_by(role_id=role_id).first()
        return get_role

    def save_user(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def register_user(cls,user_id):

        user = User.query.filter_by(id=user_id).update({
            'register':True
            })
        db.session.commit()

    @classmethod
    def get_registered_users(cls):

        users = User.query.filter_by(register=True).all()
        users_emails = []
        for user in users:
            users_emails.append(user.email)
        return users_emails
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key = True)


    article_title = db.Column(db.String)


    article_content = db.Column(db.String)
    article_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='article', lazy='dynamic', cascade="all, delete-orphan")

    def save_article(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_articles(cls):
        articles = Article.query.order_by(Article.id.desc()).all()
        return articles

    @classmethod
    def delete_articles(cls,article_id):

        comments = Comment.query.filter_by(article_id=article_id).delete()
        article = Article.query.filter_by(id=article_id).delete()
        db.session.commit()


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)

    comment_content = db.Column(db.String)

    article_id = db.Column(db.Integer, db.ForeignKey("articles.id",ondelete='CASCADE') )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,post_id):

        comments = Comment.query.filter_by(article_id=article_id).all()

        return comments

    @classmethod
    def delete_single_comment(cls,comment_id):
        comment = Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()

from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Role,Post,Comment
from .forms import CommentForm,PostForm
from flask_login import login_required,current_user
from datetime import datetime, timezone
from .. import db
import markdown2
from ..email import mail_message


@main.route('/')
def index():

    title = 'Home'
    articles= Article.get_articles()

    return render_template('index.html', title = title, articles=articles )

@main.route('/article/<int:id>')
def article(id):

    article = Article.query.get(id)
    title = f'article {article.id}'

    comments = Comment.get_comments(id)

    format_articles= markdown2.markdown(article.article_content,extras=["code-friendly", "fenced-code-blocks"])

    return render_template('article.html', title=title, article=article comments=comments, format_articles=format_articles )

@main.route('/article/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    article = Article.query.filter_by(id=id).first()

    if article is None:
        abort(404)

    form = CommentForm()

    if form.validate_on_submit():
        comment_content = form.comment_content.data
        new_comment = Comment( comment_content=comment_content, article=article, user=current_user)
        new_comment.save_comment()

        return redirect(url_for('.article', id=article.id ))

    title = 'New Comment'
    return render_template('new_comment.html', title=title, comment_form=form)

@main.route('/register/<int:id>')
@login_required
def register(id):
    user = User.query.get(id)

    if user is None:
        abort(404)

    user.register_user(id)
    return redirect(url_for('.index'))


@main.route('/blogger')
@login_required
def blogger():


    if current_user.role.id == 1 :

        title = 'Blogger'
        articles= Article.get_articles()

        return render_template('blogger.html', title = title, articles=articles)

    else:
        abort(404)

@main.route('/blogger/article/new', methods=['GET','POST'])
@login_required
def new_article():


    if current_user.role.id == 1 :

        form = ArticleForm()

        if form.validate_on_submit():
            article_title = form.article_title.data
            article_content = form.article_content.data
            new_article = Blogg(article_title=article_title, article_content=article_content, user=current_user)
            new_article.save_article()
            registered_users = User.get_registered_users()
            registered_users = ",".join(registered_users)
            mail_message("New article in the coder's haven","email/update_user",registered_users)

            return redirect(url_for('.Blogger'))

        title = 'Create article'

        return render_template('new_article.html', title = title, article_form=form )

    else:
        abort(404)

@main.route('/blogger/article/<int:id>')
@login_required
def blogger_article(id):


    if current_user.role.id == 1 :

        article = Article.query.get(id)
        title = f'article {article.id}'
        comments = Comment.get_comments(id)

        format_article= markdown2.markdown(article.article_content,extras=["code-friendly", "fenced-code-blocks"])


        return render_template('blogger_article.html', title = title, article=article, comments=comments, format_article=format_article )

    else:
        abort(404)

@main.route('/blogger/article/comment/delete/<int:id>')
@login_required
def delete_comment(id):



    if current_user.role.id == 1:

        comment = Comment.query.get(id)
        comment.delete_single_comment(id)

        return redirect(url_for('.blogger_article.html'))

    else:
        abort(404)

@main.route('/blogger/article/delete/<int:id>')
@login_required
def delete_article(id):

    if current_user.role.id == 1:

        blogg= Blogg.query.get(id)

        blogg.delete_article(id)

        return redirect(url_for('.blogger'))


    else:
        abort(404)

@main.route('/bloggerr/article/update/<int:id>' , methods=['GET','POST'])
@login_required
def update_article(id):

    if current_user.role.id == 1:

        current_article = Article.query.get(id)

        form = ArticleForm(obj=current_article)

        if form.validate_on_submit():

            form.populate_obj(current_article)

            comments = Comment.query.filter_by(article_id=id).all()
            articlet = Article.query.filter_by(id=id).update({
                'article_title': form.article_title.data,
                'article_content': form.article_content.data
                })
            db.session.commit()

            return redirect(url_for('.blogger'))

        title = 'Update article'

        return render_template('update_article.html', title = title, update_article_form=form )

    else:
        abort(404)

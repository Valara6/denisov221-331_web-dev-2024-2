from flask import Flask,Blueprint, render_template, flash, request, redirect,url_for
from flask_login import login_required, current_user
from project.run import app
from project.run import db
from math import ceil
from project.otherFunction import checkRights



bp = Blueprint('reviews', __name__, url_prefix="reviews")


REVIEWS_PER_PAGE=3

@bp.route('/<int:book_id>',methods=['GET'])
def index(book_id):
    page=int(request.args.get('page', 1))
    count=db.ExecuteQuery("SELECT count(*) as count from reviews where book=%s and review_status=2",[book_id],query_type='get')
    max_page=ceil(count[0].count/REVIEWS_PER_PAGE)
    if page>max_page and max_page!=0:
        flash("Такой страницы не существует",'danger')
        page=1
        return redirect(url_for('reviews.index', book_id=book_id,page=page))
    
    # flash(type(page))
    # flash(count[0].count)
    reviews= db.ExecuteQuery("select reviews.*, users.login as user_name from reviews join users on users.id=user where book=%s and review_status=2 LIMIT %s OFFSET %s;",[book_id,REVIEWS_PER_PAGE,((page-1)*REVIEWS_PER_PAGE)], query_type='get') 
    # flash(reviews)
    current_user_review=db.ExecuteQuery("select reviews.*, users.login as user_name from reviews join users on users.id=user where book=%s and user=%s;",[book_id, current_user.id], query_type='get')
    return render_template('reviews/index.html', reviews=reviews,
                            book_id=book_id,
                            current_user_review=current_user_review,
                            page=page,
                            count=ceil(count[0].count/REVIEWS_PER_PAGE))





@bp.route('/create/<int:book_id>', methods=['GET', 'POST'])
def create_review(book_id):
    print(book_id)
    if request.method == 'POST':
        user_id = current_user.id
        rating = request.form.get("rating")
        review_text = request.form.get("text")
        result = db.ExecuteQuery("INSERT INTO reviews (book, user, rating, text) VALUES (%s, %s, %s, %s)", [book_id, user_id, rating, review_text], query_type='post')
        if result==False:
            flash('Возникла ошибка при добавлении отзыва', 'danger')
            return redirect(url_for('.index', book_id=book_id))
        else:
            flash('Отзыв успешно добавлен', 'success')
            return redirect(url_for('.index', book_id=book_id))

    return render_template("reviews/create_review.html", book_id=book_id)



USER_REVIEWS_PER_PAGE=3

@bp.route('/MyReviews', methods=['GET'])
def MyReviews():
    page=int(request.args.get('page', 1))
    count=db.ExecuteQuery("SELECT count(*) as count from reviews where user=%s",[current_user.id],query_type='get')
    max_page=ceil(count[0].count/USER_REVIEWS_PER_PAGE)
    max_page=2
    if page>max_page and max_page!=0:
        flash("Такой страницы не существует",'danger')
        page=1
        return redirect(url_for('reviews.MyReviews', page=page))
    data = db.ExecuteQuery("select a.*, b.status, c.name from reviews a join reviews_status b on a.review_status = b.id join books c on a.book = c.id where user = %s LIMIT %s OFFSET %s", [current_user.id,USER_REVIEWS_PER_PAGE,((page-1)*USER_REVIEWS_PER_PAGE)], query_type="get" )
    return render_template("reviews/userReviews.html", data=data,page=page,count=ceil(count[0].count/USER_REVIEWS_PER_PAGE))


REQUESTS_PER_PAGE=3

@bp.route('/allreviews', methods=['GET','POST'])
@login_required
@checkRights('edit')
def allReviews():
    page=int(request.args.get('page', 1))
    count=db.ExecuteQuery("SELECT count(*) as count from reviews where review_status=1",[],query_type='get')
    max_page=ceil(count[0].count/REQUESTS_PER_PAGE)
    if page>max_page and max_page!=0:
        flash("Такой страницы не существует",'danger')
        page=1
        return redirect(url_for('reviews.allReviews', page=page))
    data = db.ExecuteQuery("select reviews.*, reviews_status.status, books.name, users.login as login from reviews join reviews_status on reviews.review_status = reviews_status.id join books on reviews.book = books.id join users on reviews.user=users.id where reviews.review_status = 1 LIMIT %s OFFSET %s",[REQUESTS_PER_PAGE,((page-1)*REQUESTS_PER_PAGE)], query_type="get" )
    return render_template("reviews/allreviews.html", data=data,page=page,count=ceil(count[0].count/REQUESTS_PER_PAGE))



@bp.route('/reviewsetstatus/<int:rev_id>', methods=['GET','POST'])
@login_required
@checkRights('edit')
def statusSetter(rev_id):
    data = db.ExecuteQuery("select a.*, b.status, c.name from reviews a join reviews_status b on a.review_status = b.id join books c on a.book = c.id where a.id = %s", [rev_id], query_type="get")
    if data == [] or data == False:
        flash("Коментария не существует", "warning")
        return redirect(url_for('reviews.allReviews'))
    return render_template('reviews/reviewviewer.html', value=data[0])






@bp.route('/status/<int:review_id>', methods=['GET', 'POST'])
@login_required
@checkRights('edit')
def status(review_id):
   
    res = request.args.get("action", "net")
  
    if not res:
        flash("Операция отклонена")
        return redirect(url_for('reviews.allReviews',page=1))

    if res == "decline":
        result = db.ExecuteQuery('UPDATE reviews SET review_status = 3 WHERE id = %s', [review_id], query_type="post")
        if result == False:
            flash("Ошибка сервера", "danger")
            return redirect(url_for('reviews.allReviews',page=1))
    elif res == "accept":
        result = db.ExecuteQuery('UPDATE reviews SET review_status = 2 WHERE id = %s', [review_id], query_type="post")
        if result == False:
            flash("Ошибка сервера", "danger")
            return redirect(url_for('reviews.allReviews', page=1))

        flash("Статус успешно обновлен", 'success')
    return redirect(url_for('reviews.allReviews', page=1))


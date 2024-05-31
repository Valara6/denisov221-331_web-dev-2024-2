from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from sqlalchemy import func,update
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]
REVIEW_PARAMS=[
    'rating','text'
]
def review_params():
    return { p: request.form.get(p) or None for p in REVIEW_PARAMS }

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }
COURSE_PER_PAGE=2
REVIEWS_PER_PAGE=3



@bp.route('/')
def index():
    pagination_type=1
    courses = CoursesFilter(**search_params()).perform()
    page=request.args.get('page',1,type=int)
    pagination = db.paginate(courses, page=page,per_page=COURSE_PER_PAGE,error_out=True)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = db.get_or_404(Course, course_id)
    reviews = db.session.execute(db.select(Review, User).join(User).filter(Review.user_id==User.id).where(Review.course_id == course_id)).scalars().fetchmany(5)
    count_review=db.session.query(Review).filter(Review.course_id==course_id).filter(Review.user_id==current_user.id).count()
    if count_review==1:
        existing_review=db.session.execute(db.select(Review, User).join(User).filter(Review.user_id==User.id).filter(Review.user_id==current_user.id).where(Review.course_id == course_id)).scalar()
        return render_template('courses/show.html', course=course,reviews=reviews, existing_review=existing_review)
    else:
        return render_template('courses/show.html', course=course,reviews=reviews, existing_review=None)

@bp.route('/<int:course_id>/show_reviews')
def show_reviews(course_id):
    sort_type=request.args.get('reviews_filter_type')
    if sort_type=='good':
        reviews = db.select(Review, User).join(User).filter(Review.user_id==User.id).where(Review.course_id == course_id).order_by(Review.rating.desc())
    elif sort_type=='bad':
        reviews = db.select(Review, User).join(User).filter(Review.user_id==User.id).where(Review.course_id == course_id).order_by(Review.rating)
    else:
        reviews = db.select(Review, User).join(User).filter(Review.user_id==User.id).where(Review.course_id == course_id).order_by(Review.created_at.desc())

    page=request.args.get('page',1,type=int)
    pagination = db.paginate(reviews, page=page,per_page=REVIEWS_PER_PAGE,error_out=True)
    reviews = pagination.items
    
    
    course = db.get_or_404(Course, course_id)
    count=db.session.query(Review).filter(Review.course_id==course_id).count()
    count_review=db.session.query(Review).filter(Review.course_id==course_id).filter(Review.user_id==current_user.id).count()
    
    
    if count_review==1:
        existing_review=db.session.execute(db.select(Review, User).join(User).filter(Review.user_id==User.id).filter(Review.user_id==current_user.id).where(Review.course_id == course_id)).scalar()
        return render_template('courses/show_reviews.html', pagination=pagination,
                                course=course,
                                reviews=reviews, 
                                count=count,
                                existing_review=existing_review,
                                reviews_filter_type=sort_type)
    else:
        return render_template('courses/show_reviews.html',
                            pagination=pagination,
                            course=course,
                            reviews=reviews,
                            count=count,
                            reviews_filter_type=sort_type,
                            existing_review=None)



@bp.route('/create_review', methods=['POST'])
def create_review():
    user_id=current_user.id
    endpoint=request.referrer
    split_path=endpoint.split('/')
    if "show_reviews" in endpoint:
        course_id=int(split_path[-2])
        flag=True
    else:
        course_id=int(split_path[-1])
        flag=False
    review=Review()
    try:
        review=Review(**review_params(),user_id=user_id,course_id=course_id)
        db.session.add(review)
        course_to_update=db.session.query(Course).filter(Course.id==course_id).one()
        course_to_update.rating_sum+=int(review.rating)
        course_to_update.rating_num+=1
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        if flag:
            return redirect(url_for('courses.show_reviews',course_id=course_id))
        else:
            return redirect(url_for('courses.show',course_id=course_id))
    flash('Отзыв был успешно добавлен!', 'success')
    if flag:
        return redirect(url_for('courses.show_reviews',course_id=course_id))
    else:
        return redirect(url_for('courses.show',course_id=course_id))
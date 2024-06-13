import hashlib
import os
import markdown
from flask import Flask, render_template, flash, send_from_directory, request, jsonify, redirect,url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import magic
from project import config
from project.auth.Auth import auth
from project.run import app
from project.run import db
from project.form import BookForm
from project.reviews import bp
import bleach
from project.otherFunction import checkRights
from math import ceil


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(bp, url_prefix='/reviews')


BOOKS_PER_PAGE=2

@app.route("/")
def index():
    page = int(request.args.get('page',1))
    count=db.ExecuteQuery("SELECT count(*) as count from books")
    
    books=db.ExecuteQuery("""
                            SELECT books.*, group_concat(genres.name) as genres_name, book_cover.filename as filename
                            FROM books
                            JOIN book_cover ON book_cover.id = books.cover
                            JOIN m2m_books_genres ON books.id = m2m_books_genres.book_id
                            JOIN genres ON m2m_books_genres.genre_id = genres.id
                            GROUP BY books.id ORDER BY books.year DESC
                            LIMIT %s OFFSET %s;
                        """,[BOOKS_PER_PAGE,((page-1)*BOOKS_PER_PAGE)],query_type='get')
    books_descriptions = {}
    ratings=db.ExecuteQuery("""SELECT books.id,books.year, IFNULL(ROUND(AVG(reviews.rating),2), 0) as avg_rating,  count(reviews.rating) as review_count 
                            from books LEFT JOIN (select * from reviews where review_status=2) as reviews on books.id=reviews.book group by books.id order by books.year DESC""")
    max_page=ceil(count[0].count/BOOKS_PER_PAGE)
    for book in range(len(books)):
        books_descriptions[book]=markdown.markdown(books[book].description)
    if page>max_page and max_page!=0:
        flash("Такой страницы не существует","danger")
        return redirect(url_for('index',page=1))
    else:
        return render_template("bookslists.html", books=books, 
                           books_descriptions=books_descriptions,
                           page=page,
                           ratings=ratings,
                           count=ceil(count[0].count/BOOKS_PER_PAGE))

#

@app.route('/create', methods=['GET', 'POST'])
@login_required
@checkRights("create")
def create():
    form = BookForm()
    genres_arr = db.ExecuteQuery("select * from genres", query_type="get")
    choices = [(genre.id, genre.name) for genre in genres_arr]
    form.genres.choices = choices

    if form.validate_on_submit():
        try:
            title = form.title.data
            description = bleach.clean(form.description.data)
            year = form.year.data
            author = form.author.data
            publisher = form.publisher.data
            pages = form.pages.data
            genres = form.genres.data

            file = request.files.get('cover')
            if file:
                flash(file.filename)
                cover_filename = secure_filename(file.filename)
                cover_path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], cover_filename)
                flash(cover_filename)
                flash(cover_path)
                file.save(cover_path)

                mime = magic.Magic(mime=True)
                cover_mime = mime.from_file(cover_path)
                with open(cover_path, 'rb') as cover_file:
                    cover_hash = hashlib.md5(cover_file.read()).hexdigest()

                existing_cover = db.ExecuteQuery("select * from book_cover where hash = %s LIMIT 1", [cover_hash], query_type="get")
                if existing_cover:
                    cover_id = existing_cover[0].id
                else:
                    db.ExecuteQuery("insert into book_cover (`filename`, `mime_type`, `hash`) values (%s, %s, %s)",
                                    [cover_filename, cover_mime, cover_hash], query_type="post")
                    cover_id = db.ExecuteQuery("select `id` from book_cover where `hash` = %s LIMIT 1", [cover_hash], query_type="get")[0].id
            else:
                flash('Отсутствует обложка книги', 'danger')
                return render_template("create.html", form=form)

            existing_book = db.ExecuteQuery("select * from books where name = %s and author = %s LIMIT 1", [title, author], query_type="get")
            if existing_book:
                flash("Такая книга уже существует", "danger")
                return render_template("create.html", form=form)

            db.ExecuteQuery("insert into books (`name`, `description`, `year`, `publisher`, `author`, `pages`, `cover`) values (%s, %s, %s, %s, %s, %s, %s)",
                            [title, description, year, publisher, author, pages, cover_id], query_type="post")

            book_id = db.ExecuteQuery("select id from books where name = %s and author = %s LIMIT 1", [title, author], query_type="get")[0].id
            for genre_id in genres:
                db.ExecuteQuery("insert into m2m_books_genres (book_id, genre_id) values (%s, %s)", [book_id, genre_id], query_type="post")

            flash('Книга успещно добавлена', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Ошибка: {e}", 'danger')
            flash('Создание отменено', 'danger')

    return render_template("create.html", form=form)

@app.route('/<int:book_id>', methods=['GET'])
def show_book(book_id):
    book=db.ExecuteQuery('select books.*, group_concat(genres.name) as genres_name, book_cover.filename as filename from books join book_cover on book_cover.id=cover join m2m_books_genres on books.id=book_id join genres on genre_id=genres.id where books.id=%s;',[book_id],query_type='get')
    ratings=db.ExecuteQuery("""SELECT IFNULL(ROUND(AVG(reviews.rating),2), 0) as avg_rating
                            from reviews where book=%s and review_status=2""",[book_id])
    book_description=markdown.markdown(book[0].description)
    return render_template('show.html',book=book, book_description=book_description,ratings=ratings)

a = "select book_id,b.name as title, description, year, publisher, author, pages, group_concat(c.name) as genre, group_concat(a.genre_id) as genres_id  from m2m_books_genres a join books b on a.`book_id` = b.id left join genres c on a.`genre_id` = c.id where a.book_id = %s;"




@app.route("/edit/<int:book_id>", methods=["POST","GET"])
@login_required
@checkRights('edit')
def edit(book_id):
    data = db.ExecuteQuery(a, params=[book_id], query_type="get")[0]
    print(data.title)
    form = BookForm(data={
        'title': data.title,
        'description': data.description,
        'year': data.year,
        'publisher': data.publisher,
        'author': data.author,
        'pages': data.pages
    })

    form.cover.validators = []
    genres_arr = db.ExecuteQuery("select * from genres", query_type="get")
    choices = [(genre.id, genre.name) for genre in genres_arr]
    form.genres.choices = choices
    if request.method == "GET" and data.genres_id:
            form.genres.data = list(map(int, data.genres_id.split(',')))
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Удаление существующих жанров
                delete_result = db.ExecuteQuery("DELETE FROM m2m_books_genres WHERE book_id=%s", [book_id], query_type='post')

                # Добавление новых жанров
                for genre_id in form.genres.data:
                    insert_result = db.ExecuteQuery("INSERT INTO m2m_books_genres (book_id, genre_id) VALUES (%s, %s)", [book_id, genre_id], query_type='post')
              
                
                # Обновление книги
                update_result = db.ExecuteQuery("UPDATE books SET name=%s, description=%s, year=%s, publisher=%s, author=%s, pages=%s WHERE id=%s", 
                                                [form.title.data, form.description.data, form.year.data, form.publisher.data, form.author.data, form.pages.data, book_id], query_type='post')
            except Exception as e:
                flash(f"Ошибка в базе данных: {e}", "danger")
            flash('Книга успешно обновлена', 'success')
            return redirect(url_for('index'))
        else:
            flash('Пожалуйста, исправьте ошибки в форме', 'danger')

    return render_template("edit.html", form=form, book_id=book_id)


@app.route("/image/<filename>", methods=["GET", "POST"])
def image(filename):
    return send_from_directory(app.config["IMAGE_UPLOAD_FOLDER"], filename)
    

@app.route('/delete_book/<int:book_id>',methods=['POST','GET'])
@login_required
@checkRights('delete')
def delete_book(book_id):
    result=db.ExecuteQuery("DELETE FROM books WHERE id=%s",[book_id],query_type='post')
    if result:
        flash('Ошибка при удалении пользователя', 'danger')
    else:
        flash('Удаление успешно', 'success')
    return redirect(url_for('index'))




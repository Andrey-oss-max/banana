from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Конфигурация для загрузки файлов
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Простые "базы данных" в памяти
messages = []
posts = []
guestbook_entries = []


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        posts.append({'title': title, 'content': content, 'author': author})
        flash('Ваше сообщение успешно опубликовано!', 'success')
        return redirect(url_for('forum'))
    return render_template('forum.html', posts=posts)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не выбран', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Изображение успешно загружено', 'success')
            return redirect(url_for('gallery'))

    # Получаем список изображений из папки uploads
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            images.append(filename)

    return render_template('gallery.html', images=images)


@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        guestbook_entries.append({'name': name, 'message': message})
        flash('Ваше сообщение добавлено в гостевую книгу!', 'success')
        return redirect(url_for('guestbook'))
    return render_template('guestbook.html', entries=guestbook_entries)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
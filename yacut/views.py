import random
import string

from flask import flash, redirect, render_template  # , url_for, abort

from . import app, db
from .forms import URL_mapForm
from .models import URL_map


DEFAULT_LINK_LENGTH = 6


def generate_alphanum_random_string(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_unique_short_id():
    # urls = URL_map.query.with_entities(URL_map.short).all()
    urls = [url.short for url in URL_map.query.all()]
    while True:
        new_url = generate_alphanum_random_string(DEFAULT_LINK_LENGTH)
        # if (new_url,) in urls:
        if new_url not in urls:
            break
    return new_url


@app.route('/<string:id>')
def get_original_url(id):
    url1 = URL_map.query.filter_by(short=id).first_or_404()
    return redirect(url1.original)


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URL_mapForm()
    context = dict()
    if form.validate_on_submit():
        if form.short.data == '':
            form.short.data = get_unique_short_id()
        if URL_map.query.filter_by(short=form.short.data).first():
            flash('Такой вариант короткой ссылки уже занят!')
            return render_template('yacut.html', form=form)
        url = URL_map(original=form.original.data, short=form.short.data)
        db.session.add(url)
        db.session.commit()
        context['url'] = url
        flash('Ваша новая ссылка готова:', 'url-done')
    context['form'] = form
    return render_template('yacut.html', **context)

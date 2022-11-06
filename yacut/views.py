import random
import string

from flask import flash, redirect, render_template

from . import app, db
from .forms import URL_mapForm
from .models import URL_map


DEFAULT_LINK_LENGTH = 6


def generate_alphanum_random_string(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_unique_short_id():
    urls = [url.short for url in URL_map.query.all()]
    while True:
        new_url = generate_alphanum_random_string(DEFAULT_LINK_LENGTH)
        if new_url not in urls:
            break
    return new_url


@app.route('/<string:id>')
def get_original_url(id):
    return redirect(URL_map.query.filter_by(short=id).first_or_404().original)


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URL_mapForm()
    custom_id = form.custom_id.data
    context = dict()
    if form.validate_on_submit():
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()
        elif URL_map.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('yacut.html', form=form)
        url = URL_map(original=form.original_link.data, short=custom_id)
        db.session.add(url)
        db.session.commit()
        context['url'] = url
        flash('Ваша новая ссылка готова:', 'url-done')
    context['form'] = form
    return render_template('yacut.html', **context)

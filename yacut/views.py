import random

from flask import flash, redirect, render_template, abort

from . import app
from .forms import URL_mapForm
from .models import URL_map


ALREADY_EXISTS = 'Имя {custom_id} уже занято!'


def generate_random_string(pattern, length):
    return ''.join(random.sample(pattern, length))


@app.route('/<string:id>')
def get_original_url(id):
    url = URL_map.get(short=id)
    if url is None:
        abort(404)
    return redirect(url.original)


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URL_mapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = 'custom_id'
    if custom_id not in form:
        abort(500)
    custom_id = URL_map.check_or_generate_short_url(form[custom_id].data)
    if URL_map.get(short=custom_id):
        flash(ALREADY_EXISTS.format(custom_id=custom_id))
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short_url=URL_map.add(
            original=form.original_link.data,
            short=custom_id
        ).get_short_url()
    )

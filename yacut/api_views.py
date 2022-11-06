import re

from flask import jsonify, request

from . import app, db
from .forms import REGEXP_ID
from .models import URL_map
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    url = data.get('url')
    custom_id = data.get('custom_id')
    if url is None or url == '':
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if custom_id is None or custom_id == '':
        custom_id = get_unique_short_id()
    elif re.match(REGEXP_ID, custom_id) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif URL_map.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Имя \"{custom_id}\" уже занято.')
    new_url = URL_map()
    new_url.original = url
    new_url.short = custom_id
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict_for_api()), 201

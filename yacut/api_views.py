# import re

from flask import jsonify, request

from . import app
from .models import URL_map
from .error_handlers import InvalidAPIUsage


NOT_FOUND_URL = 'Указанный id не найден'
EMPTY_REQUEST = 'Отсутствует тело запроса'
NO_REQUIRED_URL_FIELD = '\"url\" является обязательным полем!'
INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
ALREADY_EXISTS = 'Имя \"{custom_id}\" уже занято.'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    url = URL_map.get(short=short_id)
    if url is None:
        raise InvalidAPIUsage(NOT_FOUND_URL, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    print(data)
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    url = data.get('url')
    if url is None or url == '':
        raise InvalidAPIUsage(NO_REQUIRED_URL_FIELD)
    # Страховка реализованна в check_or_generate_short_url
    custom_id = 'custom_id'
    if custom_id in data and data[custom_id] != '':
        # try:
        custom_id = URL_map.validate_short_url(data[custom_id])
        # custom_id = URL_map.validate_short_url(
        #     URL_map.check_or_generate_short_url(data.get('custom_id', None))
        # )
    else:
        custom_id = URL_map.check_or_generate_short_url()
    # custom_id = URL_map.validate_short_url(
    #     URL_map.check_or_generate_short_url(data.get('custom_id', None))
    # )
    if custom_id is None:
        raise InvalidAPIUsage(INVALID_CUSTOM_ID)
    elif URL_map.get(short=custom_id) is not None:
        raise InvalidAPIUsage(ALREADY_EXISTS.format(custom_id=custom_id))
    return jsonify(
        URL_map.add(original=url, short=custom_id).to_dict_for_api()
    ), 201

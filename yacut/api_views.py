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
def get_url(short_id):
    url = URL_map.get(short=short_id)
    if url is None:
        raise InvalidAPIUsage(NOT_FOUND_URL, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    url = data.get('url')
    if url is None or url == '':
        raise InvalidAPIUsage(NO_REQUIRED_URL_FIELD)
    custom_id = 'custom_id'
    if (
        custom_id in data and
        data[custom_id] != '' and
        data[custom_id] is not None
    ):
        try:
            custom_id = URL_map.validate_short_url(data[custom_id])
        except (TypeError, ValueError):
            raise InvalidAPIUsage(INVALID_CUSTOM_ID)
    else:
        try:
            custom_id = URL_map.check_or_generate_short_url()
        except ValueError as error:
            raise InvalidAPIUsage(str(error))
    if URL_map.get(short=custom_id) is not None:
        raise InvalidAPIUsage(ALREADY_EXISTS.format(custom_id=custom_id))
    return jsonify(
        URL_map.add(original=url, short=custom_id).to_dict_for_api()
    ), 201

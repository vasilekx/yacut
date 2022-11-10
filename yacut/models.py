import re
from datetime import datetime

from flask import url_for
from yacut import db

from .constants import (
    CUSTOM_LINK_LENGTH,
    DEFAULT_LINK_LENGTH,
    VALID_SYMBOLS_SET,
    GENERATED_RANDOM_STRING_TRY_COUNT,
    REGEXP_ID
)
from .utilities import generate_random_string

ATTRIBUTE_ERROR_MESSAGE = (
    'Объект {class_name} не имеет атрибута {attr}.'
)
INVALID_SYMBOLS_CUSTOM_ID = (
    'Указанны недопустимые символы для короткой ссылки.'
)
INVALID_LENGTH_CUSTOM_ID = (
    f'Вариант короткой ссылки превышает {CUSTOM_LINK_LENGTH} символов.'
)
INVALID_TYPE = 'Ожидалась строка: {}'
GENERATE_URL_ERROR = (
    'Ошибка гененирования URL. Попробуйте ещё раз.'
)


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(CUSTOM_LINK_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict_for_api(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url()
        )

    def get_short_url(self):
        return url_for('get_original_url', id=self.short, _external=True)

    @staticmethod
    def _check_attributes(attrs):
        klass = URL_map
        for key in attrs:
            if not hasattr(klass, key):
                raise AttributeError(
                    ATTRIBUTE_ERROR_MESSAGE.format(
                        class_name=klass.__name__,
                        attr=key
                    )
                )

    @staticmethod
    def get(**kwargs):
        URL_map._check_attributes(kwargs.keys())
        return URL_map.query.filter_by(**kwargs).first()

    @staticmethod
    def get_unique_short_id():
        url = None
        for _ in range(GENERATED_RANDOM_STRING_TRY_COUNT):
            new_url = generate_random_string(
                VALID_SYMBOLS_SET,
                DEFAULT_LINK_LENGTH
            )
            if not URL_map.get(short=url):
                url = new_url
                break
        if not url:
            raise ValueError(GENERATE_URL_ERROR)
        return url

    @staticmethod
    def check_or_generate_short_url(custom_url=None):
        if custom_url is None or custom_url == '':
            return URL_map.get_unique_short_id()
        return custom_url

    @staticmethod
    def validate_short_url(custom_url):
        if not isinstance(custom_url, str):
            raise TypeError(INVALID_TYPE.format(custom_url))
        if re.match(REGEXP_ID, custom_url) is None:
            raise ValueError(INVALID_SYMBOLS_CUSTOM_ID)
        if len(custom_url) > CUSTOM_LINK_LENGTH:
            raise ValueError(INVALID_LENGTH_CUSTOM_ID)
        return custom_url

    @staticmethod
    def add(**kwargs):
        url = URL_map(**kwargs)
        db.session.add(url)
        db.session.commit()
        return url

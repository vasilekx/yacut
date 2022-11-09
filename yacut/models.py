import re

from datetime import datetime

from flask import url_for
from yacut import db, views

from .constants import (
    CUSTOM_LINK_LENGTH,
    DEFAULT_LINK_LENGTH,
    VALID_SYMBOLS_SET,
    GENERATED_RANDOM_STRING_TRY_COUNT,
    REGEXP_ID
)


ATTRIBUTE_ERROR_MESSAGE = (
    'Объект {class_name} не имеет атрибута {attr}.'
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
            short_link=url_for(
                'get_original_url',
                id=self.short,
                _external=True
            ),
        )

    @classmethod
    def _check_attributes(cls, attrs):
        for key in attrs:
            if not hasattr(cls, key):
                raise AttributeError(
                    ATTRIBUTE_ERROR_MESSAGE.format(
                        class_name=cls.__name__,
                        attr=key
                    )
                )

    @classmethod
    def get(cls, **kwargs):
        cls._check_attributes(kwargs.keys())
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_unique_short_id(cls):
        for _ in range(GENERATED_RANDOM_STRING_TRY_COUNT):
            url = views.generate_random_string(
                VALID_SYMBOLS_SET,
                DEFAULT_LINK_LENGTH
            )
            if not cls.get(short=url):
                break
        return url

    @classmethod
    def check_or_generate_short_url(cls, custom_url):
        if custom_url is None or custom_url == '':
            return cls.get_unique_short_id()
        return custom_url

    @classmethod
    def validate_short_url(cls, custom_url):
        return custom_url if (
            re.match(REGEXP_ID, custom_url) and
            len(custom_url) <= CUSTOM_LINK_LENGTH
        ) else None

    @classmethod
    def add(cls, **kwargs):
        url = URL_map(**kwargs)
        db.session.add(url)
        db.session.commit()
        return url

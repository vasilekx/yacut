from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from .constants import (
    REGEXP_ID,
    CUSTOM_LINK_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    VALID_SYMBOLS_SET
)


LENGHT_ERROR = (
    f'Вариант короткой ссылки не должен превышать '
    f'{CUSTOM_LINK_LENGTH} символов.'
)
REGEXP_ERROR = (
    f'Используйте следующие символы {", ".join(VALID_SYMBOLS_SET)}. '
    f'{LENGHT_ERROR}'
)
REQUIRED_INPUT_ERROR = 'Обязательное поле.'
URL_ERROR = 'Введите корректный URL-адрес.'
LENGHT_URL_ERROR = 'Превышена максимальная длина URL-адреса.'

ORIGINAL_LINK_LABEL = 'Длинная ссылка'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_BUTTON_LABEL = 'Создать'


class URL_mapForm(FlaskForm):
    original_link = StringField(
        ORIGINAL_LINK_LABEL,
        validators=[
            Length(max=MAX_ORIGINAL_LINK_LENGTH, message=LENGHT_URL_ERROR),
            DataRequired(message=REQUIRED_INPUT_ERROR),
            URL(message=URL_ERROR)
        ]
    )
    custom_id = URLField(
        CUSTOM_ID_LABEL,
        validators=[
            Length(max=CUSTOM_LINK_LENGTH, message=LENGHT_ERROR),
            Regexp(REGEXP_ID, message=REGEXP_ERROR),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_BUTTON_LABEL)

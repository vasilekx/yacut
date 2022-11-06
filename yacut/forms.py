from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp


LENGHT_ERROR = 'Вариант короткой ссылки не должен превышать 16 символов.'
REGEXP_ERROR = (f'Используяте только большие латинские буквы, '
                f'маленькие латинские буквы и '
                f'цифры в диапазоне от 0 до 9. '
                f'{LENGHT_ERROR}')
REQUIRED_INPUT_ERROR = 'Обязательное поле.'
URL_ERROR = 'Введите корректный URL-адрес.'
REGEXP_ID = r'^[0-9a-zA-Z]{0,16}$'


class URL_mapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message=REQUIRED_INPUT_ERROR),
            URL(message=URL_ERROR)
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message=LENGHT_ERROR),
            Regexp(REGEXP_ID, message=REGEXP_ERROR),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

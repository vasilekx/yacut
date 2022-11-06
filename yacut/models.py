from datetime import datetime

from yacut import db
from flask import url_for


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
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

from datetime import datetime

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])


"""
t1 = URL_map.query.with_entities(URL_map.short).filter(User.userid).all()
addr = User.query.with_entities(User.userid).filter(User.userid.like(keyword)).all()

URL_map.query.with_entities(URL_map.short).all()
[('url1',), ('url2',), ('url3',), ('url4',)]

URL_map.query.options(load_only(URL_map.short))

URL_map.query.options(load_only(URL_map.short))
"""

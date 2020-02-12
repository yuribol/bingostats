from app import db


class LocalNgrok(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    ngrok_url = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<LocalNgrok {}>'.format(self.name)

from datetime import datetime

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flasksite import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))


class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(20), nullable=False)
    forename = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'staff_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            staff_id = s.loads(token)['staff_id']
        except:
            return None
        return Staff.query.get(staff_id)

    def __repr__(self):
        return f"Staff('{self.surname}','{self.forename}','{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(20), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}', '{self.media_file}')"
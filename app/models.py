from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime
from sqlalchemy import LargeBinary
import hashlib
from markdown import markdown
import bleach


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    headline = db.Column(db.String(128))
    education = db.Column(db.String(128))
    talks_about = db.Column(db.String(128))
    # pronouns, back-image, birthday etc
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship(
        'Post', backref='author', lazy='dynamic', passive_deletes=True)
    comments = db.relationship(
        'Comment', backref='author', lazy='dynamic', passive_deletes=True)
    likes = db.relationship(
        'Like', backref='author', lazy='dynamic', passive_deletes=True)
    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(
                token.encode('utf-8'), max_age=expiration
            )
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    post_name = db.Column(db.String(100))
    post_data = db.Column(LargeBinary)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    featured = db.Column(db.Boolean, default=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    comments = db.relationship('Comment', backref="post", passive_deletes=True)
    likes = db.relationship('Like', backref="post", passive_deletes=True)

    def add_featured(self):
        self.featured = True
        db.session.add(self)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'br',
                        'h1', 'h2', 'h3', 'p'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return f'<Post {self.body[:10]}...'


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False
    )

    def __repr__(self):
        return f'<Comment {self.body[:10]}...'


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Like by {self.author}...'

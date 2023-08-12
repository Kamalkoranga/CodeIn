from api.structure import create_app
from flask_migrate import Migrate
from api.structure import db
from api.models import User, Post
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)

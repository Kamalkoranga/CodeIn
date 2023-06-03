from app import create_app
from flask_migrate import Migrate
from app import db
from app.models import User, Post

app = create_app('production')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)

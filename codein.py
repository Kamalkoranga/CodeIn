from app import create_app
from flask_migrate import Migrate
from app import db
from app.models import User, Post
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


#? For development
# if not os.path.isfile('./data-dev.sqlite'):
#     print('DB not present')
#     with app.app_context():
#         db.create_all()
#     print('DB created')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)

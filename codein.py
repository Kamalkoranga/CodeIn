import os
from app import create_app
from app import db
from app.models import User, Post
from flask import jsonify
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.route('/system_status', methods=['GET'])
def system_status():
    return jsonify({'message': "System is running properly ✅"}), 200


# ? For database creation
# if not os.path.isfile('./data.sqlite'):
#     print('DB not present')
#     with app.app_context():
#         db.create_all()
#     print('DB created')


@app.shell_context_processor
def make_shell_context():
    """The function `make_shell_context` returns a dictionary containing the
    database object `db`, the User class, and the Post class, which can be
    accessed in the Python shell.

    :return: The make_shell_context function is returning a dictionary with
    three key-value pairs. The keys are "db", "User", and "Post", and the
    values are the corresponding objects or classes associated with those keys.
    """
    return dict(db=db, User=User, Post=Post)


if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_migrate import Migrate

from book.models import init_app, db
from book.routes import book_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lmkCgJFJ3nVec_w4bnn-bA'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/book.db'

app.register_blueprint(book_blueprint)
init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=False, port=5001)

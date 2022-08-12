from flask import Flask
from flask_migrate import Migrate

from order.models import init_app, db
from order.routes import order_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '8WfrzCBcIpagDFrAp87U7w'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/order.db'

app.register_blueprint(order_blueprint)

init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=False, port=5002)

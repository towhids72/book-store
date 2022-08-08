import base64

from flask import Flask, g
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager
from flask_migrate import Migrate

from user import models
from user.routes import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lmkCgJFJ3nVec_w4bnn-bA'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
models.init_app(app)
app.register_blueprint(user_blueprint)
login_manager = LoginManager(app)
migrate = Migrate(app, models.db)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


if __name__ == '__main__':
    app.run()

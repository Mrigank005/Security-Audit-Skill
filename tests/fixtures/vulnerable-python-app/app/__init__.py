from flask import Flask
from app.routes.users import users_bp
from app.routes.auth import auth_bp, SECRET_KEY
from app.utils.render import render_bp

app = Flask(__name__)

app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(render_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

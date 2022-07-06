from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    from api.routes import api
    from main.routes import main
    app.register_blueprint(api)
    app.register_blueprint(main)

    return app

app = create_app()
app.secret_key = os.environ.get('SECRET')

if __name__ == '__main__':
    app.run()
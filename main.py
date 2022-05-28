from flask import Flask

def create_app():
    app = Flask(__name__)

    from api.routes import api
    from main.routes import main
    app.register_blueprint(api)
    app.register_blueprint(main)

    return app

app = create_app()
app.secret_key = "shhh"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
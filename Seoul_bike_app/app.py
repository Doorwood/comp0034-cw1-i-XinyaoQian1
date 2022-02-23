# from flask import Flask
from Seoul_bike_app import create_app, config

app = create_app(config.DevelopmentConfig)


@app.route('/')
def index():
    return 'hello this is default home page'


if __name__ == '__main__':
    app.run(debug=True, port=8080)

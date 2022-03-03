from flask import render_template
from Seoul_bike_app import create_app, config

app = create_app(config.DevelopmentConfig)


@app.route('/')
def index():
    return render_template('index.html',title= 'Home Page')


@app.route('/reporter/<int:reporter_id>')
def reporter(reporter_id):
    return f'''
    <h2>Reporter {reporter_id} Bio</h2>
    <a href="/">Return to home page</a>
    '''


if __name__ == '__main__':
    app.run(debug=True, port=8080)

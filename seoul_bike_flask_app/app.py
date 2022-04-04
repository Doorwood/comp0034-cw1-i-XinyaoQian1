# import sys
# sys.path.insert(0,"..")

from seoul_bike_flask_app import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)



if __name__ == '__main__':
    app.run(debug=True,port=5050)
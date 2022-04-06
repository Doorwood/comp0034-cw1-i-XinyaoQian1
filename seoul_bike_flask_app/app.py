"""
# @File    :    app.py
# @Time    :    24/02/2022 01:36
# @Author  :    Xinyao Qian
# @SN      :    19021373
# @Description:
"""
from seoul_bike_flask_app import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)


if __name__ == '__main__':
    app.run(debug=True,port=5050)

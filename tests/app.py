from flask import Flask
from blue import blue_route
from common.lib import UrlManager

from flask_sqlalchemy import SQLAlchemy

# __name__是用来确定flask运行的主文件
app = Flask(__name__)

app.register_blueprint(blue_route,url_prefix="/flow")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/mysql'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    url = UrlManager.buildUrl("/api")
    return 'Hello World!'+url

@app.route('/api')
def api():  # put application's code here
    app.logger.debug("api warning")
    return 'api!'

@app.route('/api/hello')
def index():  # put application's code here
    sql = "SELECT * FROM `user`"
    result = db.engine.execute(sql)

    for row in result:
        app.logger.info(row)

    return 'index!'

@app.errorhandler(404)
def page_not_found(error):
    return 'page 404'
if __name__ == '__main__':
    app.run(host='0.0.0.0')

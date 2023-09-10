from flask import Flask,redirect,url_for
from app.routes.main_routes import app_views
from app.config import *

app = Flask(__name__)
app.register_blueprint(app_views)


# 定义上下文全局变量
@app.context_processor
def inject_global_variables():
    greeting = {
        "title":STYLE_TITLE,
        "subdomain": STYLE_SUBDOMAIN,
        "rootDomain": STYLE_ROOTDOMAIN,
        "backgroundColor": STYLE_BACKGROUNGCOLOR,
        "primaryColor": STYLE_PRIMARYCOLOR
    }
    return dict(greeting=greeting)
# 处理 404 错误的函数
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('app_views.index'))  # 重定向到根路径


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)

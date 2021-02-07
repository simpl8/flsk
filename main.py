from flask import Flask, render_template, request, redirect, session
from settings import Config
from werkzeug.routing import BaseConverter
import requests


# 1.实例化flask应用对象
app = Flask(__name__)
app.config.from_object(Config)


# 2.编写视图和路由
@app.route(rule="/", methods=["get", "post"])
def index():
    return "<h1>hello Flask</h1>"


# 将路由传递的user_id(int类型)返回
@app.route(rule="/user/<int:user_id>", methods=["get"])
def user(user_id):
    return f"hello {user_id}"


# 自定义路由转换器
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8990)
    # print(app.config.from_object('settings.Config'))



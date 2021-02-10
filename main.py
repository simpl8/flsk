from flask import Flask, render_template, request, redirect, session
from settings import Config
from loguru import logger
import requests
# 1，引入BaseConverter路由参数转换器基类
from werkzeug.routing import BaseConverter


# 1.实例化flask应用对象
app = Flask(__name__)
# 1.1 加载配置到应用对象中
app.config.from_object(Config)


# 2.编写视图和路由
@app.route(rule="/", methods=["get", "post"]) # 
def index():
    logger.info(request.method)
    logger.info(request.data)
    logger.info(f"输入的字符串为：{request.query_string},{type(request.query_string)}")
    logger.info(f"输出args:{request.args},类型：{type(request.args)}")
    logger.info(f"拿到args里边的值：{request.args.get('name')}")
    logger.info(f"ajax请求的json数据：{request.json}")
    return f"<h1>hello {request.args}</h1>"


# 将路由传递的user_id(int类型)返回
@app.route(rule="/user/<string:user_id>", methods=["get"])
def user(user_id):

    return f"hello {user_id}"


# 自定义路由转换器
# 2，自定义路由参数转换器
class MobileConverter(BaseConverter):
    regex = r"1[3-9]\d{9}"

    def __init__(self, map, *args, **kwargs):
        super().__init__(map, *args, **kwargs)


# 3，注册路由参数转换到app应用对象, url_map是flask路由列表对象，类似于Django里的urlpatterns
app.url_map.converters["mobile"] = MobileConverter
@app.route(rule="/phone/<mobile:tel_phone>")
def user_mobile(tel_phone):
    return f"hello you {tel_phone}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8990)
    # print(app.config.from_object('settings.Config'))



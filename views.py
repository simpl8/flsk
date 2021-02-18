from flask import Flask, render_template, request, redirect, session, url_for, make_response, abort, current_app
from flask_wtf import CSRFProtect
from settings import Config
from loguru import logger
# 1，引入BaseConverter路由参数转换器基类
from werkzeug.routing import BaseConverter
from flask import jsonify
from flask_script import Manager, Command
from flask_sqlalchemy import SQLAlchemy


# 1.实例化flask应用对象
app = Flask(__name__)
# 实例化CSRFProtect
CSRFProtect(app)
# 1.1 加载配置到应用对象中
app.config.from_object(Config)
#app.config.from_object(DbConfig)
manage = Manager(app)
# db = SQLAlchemy(app)


class DbConfig:
    # 数据库链接配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Suhang1908@182.254.241.179:3306/simple_dev?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


app.config.from_object(DbConfig)
db = SQLAlchemy(app)


# 数据库迁移,项目要通过manage启动
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate()
migrate.init_app(app, db)
manage.add_command("db", MigrateCommand)


# 创建学生类，即学生表
class Student(db.Model):
    __tablename__ = "db_student"  # 数据库表名
    id = db.Column(db.Integer, primary_key=True, comment="ID")
    name = db.Column(db.String(64), index=True, comment="姓名")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    age = db.Column(db.Integer, nullable=True, comment="年龄")
    email = db.Column(db.String(128), nullable=True, comment="邮箱")
    money = db.Column(db.Numeric(8, 2), default=0, comment="钱包")
    
    # 模型方法
    def __repr__(self):
        return f"{self.name}"

# 2.编写视图和路由
@app.route(rule="/", methods=["get", "post"]) # 
def index():
    # abort(404)  # 抛出错误异常，一般用于权限等页面上的错误展示提示（业务层面）
    logger.info(request.method)
    logger.info(request.data)
    logger.info(f"输入的字符串为：{request.query_string},{type(request.query_string)}")
    logger.info(f"输出args:{request.args},类型：{type(request.args)}")
    logger.info(f"拿到args里边的值：{request.args.get('name')}")
    logger.info(f"ajax请求的json数据：{request.json}")
    logger.info(request.is_json)
    title = "欢迎来到首页"
    username = "simple"
    return render_template("login.html")  # 将数据传到客户端


# 登录视图
@app.route("/login", methods=["post"])
def login():
    logger.info(request.form)
    return "ok"


# 添加数据到Student
@app.route("/student_add")
def student_add():
    # 添加一个学生到数据库中
    #student = Student(name="simple", sex=True, age=28, email="s1mp1e@126.com", money=1000)
    st1 = Student(name="SuHang", sex=False, age=26, email="s1mp1e@126.com", money=1000)
    st2 = Student(name="FangZheng", sex=True, age=29, email="s1mp1e@126.com", money=1000)
    #db.session.add(student)
    db.session.add_all([st1, st2])
    db.session.commit()  # 提交信息
    return f"添加成功"
    
    
# 数据库查询操作
@app.route("/student_query")
def query_student():
    student = Student.query.get(2)  # 查询主键为2的数据
    logger.info(student)
    return f"{student}"
    

# 数据库删除操作
@app.route("/student_delete")
def del_student():
    # 方法一
    # try:
    #     student = Student.query.get(4)
    #     db.session.delete(student)
    #     db.session.commit()
    # except Exception:
    #     return f"数据不存在"
    # return f"{student}删除成功"
    # 方法二，事务操作，乐观锁
    Student.query.filter(Student.name == "FangZheng").delete()
    db.session.commit()
    return "ok"


# 数据库更新
@app.route("/student_update")
def student_update():
    Student.query.filter(Student.name == "SuHang").update({"name": "ZhangSuHang"})
    db.session.commit()
    return "更新成功"


# 购物车视图
@app.route("/index/goodscart")
def goodscart():
    goods = {"name": ["python", "java", "rust"],
             "price": [50, 60, 70]
             }
    if request.args.get("password") == "1908":
        return render_template("goodscart.html", goods=goods)
    else:
        return "对不起，您无权访问该购物车"
# 将路由传递的user_id(int类型)返回
@app.route(rule="/user/<string:user_id>", methods=["get"])
def user(user_id):
    return f"hello {user_id}"


# 手机号屏蔽页面
@app.route("/mobile_mask")
def mask():
    mobile = '18621837214'
    return render_template("mobile_mask.html", mobile=mobile)


# 屏蔽手机号中间四位的自定义过滤器
@app.template_filter("mask")
def do_mobile(data, string="****"):
    return data[:3] + string + data[7:]


@app.route(rule="/user/json", methods=["get", "post"])
def json_res():
    data = {"name": "simple", "age": 18}
    return jsonify(data)


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


# 4, 重定向
@app.route("/red", methods=["get", "post"])
def red():
    # return redirect("http://www.baidu.com")
    # return redirect(url_for("json_res"))  # 通过url_for("视图名")实现视图方法之间的内部跳转
    return redirect(url_for(endpoint="user_mobile", tel_phone=13387676567))  # 带参数的视图方法跳转


# 5, flask提供的http会话控制cookie
@app.route("/cook")
def cook():
    response = make_response("ok")
    # response.set_cookie("键"， "值"， "有效期(单位秒)")
    response.set_cookie("username", "simple")  # 没有设置有效期，默认为会话期，关闭浏览器过期
    return response


# 读取cookie
@app.route("/read_cook")
def cookie_read():
    print(request.cookies)
    return "ok"


# 使用session前必须先设置密钥
class SessionConfig:
    SECRET_KEY = "LJLAJFOWIENOWWN"
    
    
app.config.from_object(SessionConfig)


# 6, 设置session
@app.route('/set_session')
def set_session():
    session["username"] = 'simple'
    return "ok"


# 读取session
@app.route("/get_session")
def get_session():
    print(session["username"])
    return "ok"


# 删除session
@app.route("/del_session")
def del_session():
    session.pop("username")
    return "ok"
    
    
# 7, 请求钩子
# 7.1 before_first_request
@app.before_first_request
def first_request():
    # 网站运行后，第一个请求执行之前的操作，主要用于写全局初始化代码
    print('数据库链接')
    print('网站全局缓存')


# 7.2 before_request
@app.before_request
def every_request():
    # 每次客户端请求前
    print("判断权限")
    print("识别用户身份")
    

# 7.3 after_request
@app.after_request
def every_response(response):
    print("日志记录")
    print("操作历史记录")
    print("备份操作")
    return response
    
    
# 7.4 teardown_request
@app.teardown_request
def teardown_request(exc):
    print('异常处理')
    

# 捕获异常，例如之前index视图抛出404，进行异常处理
# @app.errorhandler(404)
# def exe_error1(e):
#     logger.debug("错误异常了")
#     return "sorry page not found"
    

# current_app
@app.route("/current")
def app_current():
    print(current_app.config)
    return f"{current_app.config}"
# 8 flask_script

    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1908)
    # print(app.config.from_object('settings.Config'))
    # manage.run()



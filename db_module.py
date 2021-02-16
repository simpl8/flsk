from views import app
from flask_sqlalchemy import SQLAlchemy


class DbConfig:
    # 数据库链接配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Suhang1908@182.254.241.179:3306/simple_dev?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    

app.config.from_object(DbConfig)
db = SQLAlchemy(app)


# 创建学生类，即学生表
class Student(db.Model):
    __tablename__ = "db_student"
    id = db.Column(db.Integer, primary_key=True, comment="ID")
    name = db.Column(db.String(64), index=True, comment="姓名")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    age = db.Column(db.Integer, nullable=True, comment="年龄")
    email = db.Column(db.String(128), nullable=True, comment="邮箱")
    money = db.Column(db.Numeric(8, 2), default=0, comment="钱包" )

    # 模型方法
    def __repr__(self):
        return f"{self.name}"
    
    
# if __name__ == "__main__":
#     with app.app_context():  # 一定要在app上下文内执行数据库创建
#         # 创建表结构
#         db.create_all()
        # db.drop_all()  # 删除所有模型对应的数据表结构
        
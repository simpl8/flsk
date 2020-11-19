from flask import Flask
import functools


app = Flask(__name__)


# 不带参数的装饰器
def wapper(func):
    @functools.wraps(func) # 将原函数的信息赋值给inner
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner


'''
1, 执行wapper函数，并将被装饰器装饰的函数当作参数传递给wapper：wapper(index)
2, 将第一步的返回值，重新赋值给新index， index = wapper(老index)
'''
@wapper
def index(ax):
    return ax +1000


class animal:

    def __init__(self, foot, hand):
        self.foot = foot
        self.hand = hand

    def hande(self):
        msg = f"i have 1 {self.hand}"
        return msg

    def foote(self):
        msg = f"i have 4 {self.foot}"
        return msg


if __name__ == "__main__":
    tiger = animal(4, 1)
    print(tiger.hande())
from flask import Flask, render_template, request, redirect, session


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.debug = True

USER_DICT = {
    "1": {"name": "hanJun", "age": 18},
    "2": {"name": "haoHan", "age": 28},
    "3": {"name": "anQi", "age": 38}
}


@app.route('/login', methods=['GET', 'POST'])  # methods: 允许请求的方法，默认为get
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'alex' and pwd == '123':
        session['user_info'] = user  # session默认放在浏览器cookie里边
        return redirect('/index')
    else:
        return render_template('login.html', msg='用户名或密码错误')


@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('/login')


@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return render_template('/index.html', user_dict=USER_DICT)


@app.route('/detail')
def detail():
    user_info = session.get('user_info')
    if not user_info:
        return redirect("/login")
    uid = request.args.get("uid")
    info = USER_DICT.get(uid)
    return render_template("/detail.html", info=info)


if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, request, redirect, session
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
# app.debug = True


@app.route('/login', methods=['GET', 'POST'])  # methods: 允许请求的方法，默认为get
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'simple' and pwd == '123456':
        session['user_info'] = user  # session默认放在浏览器cookie里边
        return redirect('/tools')
    else:
        return render_template('login.html', msg='用户名或密码错误!')


@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('/login')


@app.route('/index')
def index():
    user_info = session.get('user_info')
    book = {
        "《Python》": "40",
        "《Java》": "35",
    }

    if not user_info:
        return redirect('/login')
    return render_template('index.html', user=user_info, books=book)


# "url": "http://iyb-icarus.test.za-tech.net/int/v1/rule/formula/run",
# "url": "http://iyb-icarus.pre.za-tech.net/int/v1/rule/formula/run",
@app.route('/tools', methods=['GET', 'POST'])
def tools():
    if request.method == 'GET':
        return render_template('tools.html')
    interface = request.form.get('inter')
    policy_no = request.form.get("policyNo")
    body = {
        "method": "post",
        "url": interface,
        "json": {
            "code": "saasCommissionBatchStatus1to2",
            "context": {
                "ownerCompany": 18,
                "policyNo": policy_no
            }
        }
    }
    result_msg = requests.request(**body).json()
    return render_template('tools.html', msg=result_msg)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="4999", debug=True)